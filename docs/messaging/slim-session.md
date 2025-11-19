# SLIM Sessions

This document explains the SLIM session layer and the two supported session
types. It helps you understand the two session interfaces, reliability, and security trade‑offs.

The SLIM repository ships with practical, runnable [examples](https://github.com/agntcy/slim/tree/slim-v0.7.0/data-plane/python/bindings/examples) that demonstrate how to create sessions and exchange messages between applications using the Python bindings.

## Point-to-Point Session

The point-to-point session enables point-to-point communication with a specific
instance. This session performs a discovery phase to bind to one instance and all
subsequent traffic in the session targets that same endpoint. With reliability
enabled, each message in the session must be acked.

If MLS is enabled, the point-to-point session establishes a two‑member MLS group after
discovery. This mirrors the Group flow but with only two participants
(see [Group Session](#group-session)).

The diagram below illustrates a point-to-point session from App-A to agntcy/ns/App-B.
App-A first discovers an available instance (App-B/1), then performs the MLS
setup, and finally sends multiple messages to that same instance, each followed
by an Ack. If MLS is not enabled, the MLS setup is skipped.

```mermaid
sequenceDiagram
    autonumber

    participant App-A
    participant SLIM Node
    participant App-B/1
    participant App-B/2

    Note over App-A,App-B/2: Discovery
    App-A->>App-A: Init MLS state
    App-A->>SLIM Node: Discover agntcy/ns/App-B
    SLIM Node->>App-B/1: Discover agntcy/ns/App-B
    App-B/1->>SLIM Node: Discover Reply (agntcy/ns/App-B/1)
    SLIM Node->>App-A: Discover Reply (agntcy/ns/App-B/1)

    Note over App-A,App-B/2: Invite
    App-A->>SLIM Node: Invite agntcy/ns/App-B/1
    SLIM Node->>App-B/1: Invite agntcy/ns/App-B/1
    App-B/1->>App-B/1: Create new point-to-point Session
    App-B/1->>SLIM Node: Invite Reply (MLS key package)
    SLIM Node->>App-A: Invite Reply (MLS key package)
    App-A->>App-A: Update MLS state

    Note over App-A,App-B/2: MLS setup
    App-A->>SLIM Node: MLS Welcome agntcy/ns/App-B/1
    SLIM Node->>App-B/1: MLS Welcome agntcy/ns/App-B/1
    App-B/1->>App-B/1: Init MLS state
    App-B/1->>SLIM Node: Ack(MLS Welcome)
    SLIM Node->>App-A: Ack(MLS Welcome)

    Note over App-A,App-B/2: Message exchange
    App-A->>SLIM Node: Message to agntcy/ns/App-B/1
    SLIM Node->>App-B/1: Message to agntcy/ns/App-B/1
    App-B/1->>SLIM Node: Ack
    SLIM Node->>App-A: Ack

    App-A->>SLIM Node: Message to agntcy/ns/App-B/1
    SLIM Node->>App-B/1: Message to agntcy/ns/App-B/1
    App-B/1->>SLIM Node: Ack
    SLIM Node->>App-A: Ack
```

### Create a Point-to-Point Session

Using the SLIM Python bindings, you can create a point-to-point session as follows:

```python
config = slim_bindings.SessionConfiguration.PointToPoint(
    max_retries=5,
    timeout=datetime.timedelta(seconds=5),
    mls_enabled=enable_mls,
)
session, handle = await local_app.create_session(remote_name, config)
await handle
```

Config Parameters:

* `max_retries` (optional, int): Retry attempts per message if Ack missing.
* `timeout` (optional, timedelta): Wait per attempt for an Ack before retry.
    If `timeout` is not set, the session is best‑effort.
* `mls_enabled` (optional, bool): Enable end‑to‑end encryption (MLS).

Create Session Parameters:

* `remote_name` (required, Name): Identifier of the remote participant
    instance.
* `config` (required, SessionConfiguration): The configuration object created for this session.

The `await handle` guarantees that once returned all the underlying message exchange
is done and the remote is correctly connected to the session.

### Sending and Replying in a Point-to-Point Session

As the point-to-point session is bound to a single remote instance after discovery,
outbound messages use the implicit destination. Use `publish` for normal sends
and to reply back to the sender.

This example shows how to send and reply in a point-to-point session:

```python
# Send a message using publish; it will reach the endpoint
# specified at session creation
await session.publish(b"hello")

# Await reply from remote (pattern depends on your control loop)
msg_ctx, payload = await session.get_message()
print(payload.decode())

# Send a correlated response back (echo style)
# The message will be sent according to the info in the session
await session.publish(payload)
```

### Point-to-Point Example

This [example](https://github.com/agntcy/slim/blob/slim-v0.7.0/data-plane/python/bindings/examples/src/slim_bindings_examples/point_to_point.py) walks through the creation of a point-to-point session. When running the point-to-point example multiple times, the session binds to different running instances, while the message stream always sticks to the same endpoint.

The example demonstrates how to publish messages, enable reliability, and enable MLS for end‑to‑end security. The associated [README](https://github.com/agntcy/slim/blob/slim-v0.7.0/data-plane/python/bindings/examples/src/slim_bindings_examples/README_point_to_point.md) shows more information and how to run the example using the Taskfile provided in the repository.

## Group Session

The Group session allows many-to-many communication on a named channel. Each
message is delivered to all participants connected to the same session.

The creator of the channel can act as a moderator, meaning that it can add or
remove participants from the session. Moderation can be built into your application
or delegated to a separate control service or the SLIM control plane.

Below are examples using the latest Python bindings, along with explanations of
what happens inside the session layer when a participant is added or removed
from the channel (see [Group management](./slim-group.md)).

### Create a Group Session

To create a group session, you need to configure the session with a topic
name and specify reliability and security settings. Here is an
example:

```python
config = slim_bindings.SessionConfiguration.Group(
    max_retries=5,  # Max per-message resend attempts upon missing ack before reporting a delivery failure.
    timeout=datetime.timedelta(
        seconds=5
    ),  # Ack / delivery wait window; after this duration a retry is triggered (until max_retries).
    mls_enabled=enable_mls,  # Enable Messaging Layer Security for end-to-end encrypted & authenticated group communication.
)

created_session, handle = await local_app.create_session(
    chat_channel,  # Logical group channel (Name) all participants join; acts as group/topic identifier.
    config,  # session configuration
)

await handle
```

Config Parameters:

* `max_retries` (optional, int): Retry attempts per message if Ack missing.
* `timeout` (optional, timedelta): Wait per attempt for an Ack before retry.
    If `timeout` is not set, the session is best‑effort.
* `mls_enabled` (optional, bool): Enable end‑to‑end encryption (MLS).

Create Session Parameters:

* `chat_channel` (required, Name): Identifier of the group channel that all
    participants join.
* `config` (required, SessionConfiguration): The configuration object created for this session.

As in the case of point to point session, the `await handle` guarantees that once returned all the 
underlying message exchange is completed.

### Sending and Replying in a Group Session

In a Group, the session targets a channel: all sends are delivered to all the current
participants. Use `publish` to send a message to all the participants in the group.

```python
# Broadcast to the channel
await session.publish(b"hello")

# Handle inbound messages
msg_ctx, data = await session.get_message()
print("channel received:", data.decode())
```

### Invite a New Participant

The creator of the session can invite a new participant to the channel using the `invite`
method after creating the session.

```python
# After creating the session:
for invite in invites:
    invite_name = split_id(invite)
    await local_app.set_route(invite_name)
    handle = await created_session.invite(invite_name)
    await handle
    print(f"{local} -> add {invite_name} to the group")
```

Parameters:

* `invite_name` (required, Name): Identifier of the participant to add.

Notice the `await local_app.set_route(invite_name)` command before the invite.
This instructs SLIM on how to forward a message with the specified name.
This has to be done by the application for every invite.

The `await handle` returns once the remote participant is correctly added to the
group and all the state on every participant is updated. In fact,
when a moderator wants to add a new participant (e.g., an instance of App-C) to
a group session, all the following steps need to be executed (see diagram below):

1. **Discovery Phase:** The moderator initiates a discovery request to find a
    running instance of the desired application (App-C). This request is sent to
    the SLIM Node, which forwards it via anycast to one of the App-C instances.
    In the example, the message is forwarded to App-C/1 that replies with its
    full identifier. The SLIM Node relays this reply back to the moderator.

2. **Invitation:** The moderator sends an invite message for the discovered
    instance (App-C/1) to the SLIM Node, which forwards it to App-C/1. Upon
    receiving the invite, App-C/1 creates a new group session, subscribes to
    the channel, and replies with its MLS (Messaging Layer Security) key
    package. This reply is routed back to the moderator.

3. **Group State Update:** The moderator initiates an MLS commit to add App-C/1
    to the secure group. The message is sent using the channel name and so the
    SLIM Node distributes this commit to all current participants (App-B/2 and
    App-A/1), who update their MLS state and acknowledge the commit. This message
    also contains the new list of participants in the group, in particular the
    newly added participant. The
    moderator collects all acknowledgments for the update message. Once all acknowledgments are
    received, the moderator sends an MLS Welcome message to App-C/1. App-C/1
    initializes its MLS state, gets the current list of participants in the group
    and acknowledges receipt. At the end of this
    process, all participants (including the new one) share a secure group state
    and can exchange encrypted messages on the group channel. If MLS is
    disabled, the update and welcome messages are used only to exchange the new list of
    participants in the group, so that they are all aware of who is connected.

```mermaid
sequenceDiagram
    autonumber

    participant Moderator
    participant SLIM Node
    participant App-C/1
    participant App-C/2
    participant App-B/2
    participant App-A/1

    Note over Moderator,App-A/1: Discovery
    Moderator->>SLIM Node: Discover agntcy/ns/App-C
    SLIM Node->>App-C/1: Discover agntcy/ns/App-C
    App-C/1->>SLIM Node: Discover Reply from agntcy/ns/App-C/1
    SLIM Node->>Moderator: Discover Reply from agntcy/ns/App-C/1

    Note over Moderator,App-A/1: Invite
    Moderator->>SLIM Node: Invite agntcy/ns/App-C/1
    SLIM Node->>App-C/1: Invite agntcy/ns/App-C/1
    App-C/1->>App-C/1: Create new Group session
    App-C/1->>SLIM Node: Subscribe to Channel
    App-C/1->>SLIM Node: Invite Reply (MLS key package)
    SLIM Node->>Moderator: Invite Reply (MLS key package)
    Moderator->>Moderator: Update MLS state

    Note over Moderator,App-A/1: Group State Update
    Moderator->>SLIM Node: Group Update (Add agntcy/ns/App-C/1, MLS commit) to Channel
    par Group State Update on App-C/1
        SLIM Node->>App-B/2: Group Update (Add agntcy/ns/App-C/1, MLS commit) to Channel
        App-B/2->>App-B/2: Update Group and MLS state
        App-B/2->>SLIM Node: Ack(Group Update)
        SLIM Node->>Moderator: Ack(Group Update)
    and Group State Update on App-A/1
        SLIM Node->>App-A/1: Group Update (Add agntcy/ns/App-C/1, MLS commit) to Channel
        App-A/1->>App-A/1: Update Group and MLS state
        App-A/1->>SLIM Node: Ack(Group Update)
        SLIM Node->>Moderator: Ack(Group Update)
    end
    Moderator->>SLIM Node: Welcome agntcy/ns/App-C/1
    SLIM Node->>App-C/1: Welcome agntcy/ns/App-C/1
    App-C/1->>App-C/1: Init Group and MLS state
    App-C/1->>SLIM Node: Ack(Welcome)
    SLIM Node->>Moderator: Ack(Welcome)
```

### Remove a Participant

A moderator can remove a participant from the channel using the `remove`
method after creating the session.

This example shows how to remove a participant from a group session:

```python
# To remove a participant from the session:
await session.remove(remove_name)
```

Parameter:

* `remove_name` (required, Name): Identifier of the participant to remove.

When a moderator wants to remove a participant (e.g., App-C/1) from a group
session, the following steps occur. All the steps are visualized in the diagram
below:

1. **Group State Update:** The moderator creates an MLS commit to remove App-C/1
    from the secure group. This commit is sent to the group channel and the
    SLIM Node distributes it to all current participants (App-C/1, App-B/2, and
    App-A/1). The message also contains the name of the participant to remove so
    that all the endpoints can update their list of participants.
    Each participant updates its MLS state and acknowledges the
    commit. The moderator collects all acknowledgments. If MLS is
    disabled, only the name of the participant to remove is sent using this message.

2. **Removal:** After the MLS state is updated, the moderator sends a remove
    message to App-C/1. Upon receiving the remove message, App-C/1 unsubscribes
    from the channel, deletes its group session, and replies with a
    confirmation. The SLIM Node relays this confirmation back to the moderator.
    At the end of this process, App-C/1 is no longer a member of the group
    and cannot send or receive messages on the channel.

```mermaid
sequenceDiagram
    autonumber

    participant Moderator
    participant SLIM Node
    participant App-C/1
    participant App-B/2
    participant App-A/1

    Note over Moderator,App-A/1: Group State Update
    Moderator->>SLIM Node: Group Update (Remove agntcy/ns/App-C/1, MLS commit) to Channel
    par Handle Group State Update on App-C/1
        SLIM Node->>App-C/1: Group Update (Remove agntcy/ns/App-C/1, MLS commit) to Channel
        App-C/1->>App-C/1: Update Group and MLS state
        App-C/1->>SLIM Node: Ack(Group Update)
        SLIM Node->>Moderator: Ack(Group Update)
    and Handle Group State Update on App-B/2
        SLIM Node->>App-B/2: Group Update (Remove agntcy/ns/App-C/1, MLS commit) to Channel
        App-B/2->>App-B/2: Update Group and MLS state
        App-B/2->>SLIM Node: Ack(Group Update)
        SLIM Node->>Moderator: Ack(Group Update)
    and Handle Group State Update on App-A/1
        SLIM Node->>App-A/1: Group Update (Remove agntcy/ns/App-C/1, MLS commit) to Channel
        App-A/1->>App-A/1: Update Group and MLS state
        App-A/1->>SLIM Node: Ack(Group Update)
        SLIM Node->>Moderator: Ack(Group Update)
    end

    Note over Moderator,App-A/1: Remove
    Moderator->>SLIM Node: Remove agntcy/ns/App-C/1
    SLIM Node->>App-C/1: Remove agntcy/ns/App-C/1
    App-C/1->>SLIM Node: Unsubscribe from Channel
    App-C/1->>App-C/1: Remove Group session
    App-C/1->>SLIM Node: Remove Reply
    SLIM Node->>Moderator: Remove Reply
```

If the moderator is removed from the group, or it simply closes the session, it sends a
close message on the channel that is received by all the group participants. Upon reception,
all the participants acknowledge that the message was received and they close the local session,
similar to the reception of the remove message (see the diagram). In this way, when the moderator
stops, all participants are removed from the group.

### Group Example

This [example](https://github.com/agntcy/slim/blob/slim-v0.7.0/data-plane/python/bindings/examples/src/slim_bindings_examples/group.py) demonstrates how to create a group session, invite participants, and (if enabled) establish an MLS group for end-to-end encryption. It also shows how to broadcast messages to all current members and handle inbound group messages. The associated [README](https://github.com/agntcy/slim/blob/slim-v0.7.0/data-plane/python/bindings/examples/src/slim_bindings_examples/README_group.md) shows more information and how to run the example using the Taskfile.
