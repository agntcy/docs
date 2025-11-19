# SLIM Group Creation and Management

One of the key features of [SLIM](slim-core.md) is its support for secure group communication.
In SLIM, a group consists of multiple clients that communicate through a shared
channel. Each channel is identified by a unique name, as described in the [SLIM
Messaging Layer](slim-data-plane.md). When MLS is enabled, group
communication benefits from end-to-end encryption.

This guide provides all the information you need to create and manage groups within a
SLIM network. A full tutorial with examples is available in
[Group Communication Tutorial](./slim-group-tutorial.md).

## Creating Groups with the Python Bindings

This section shows how to use the SLIM Python bindings to create a group.
This requires a [group session](./slim-session.md#group-session). A group
session is a channel shared among multiple participants and used to
send messages to everyone. When a new participant wants to join the channel,
they must be invited by the channel creator.

The channel creator can be part of a Python application and can either
actively participate in the communication process (possibly implementing some
of the application logic) or serve solely as a channel moderator.

This section provides the basic
steps to follow, along with Python code snippets, for setting up a group session.
The full code is available in the [group.py](https://github.com/agntcy/slim/blob/slim-v0.7.0/data-plane/python/bindings/examples/src/slim_bindings_examples/group.py) example in the SLIM repository.

### Create the Channel

The channel can be created with a group session,
which initializes the corresponding state in the SLIM session layer.
In a group session, communication between participants can be encrypted
end-to-end, enabling MLS.

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

await handle # await for the session to be created
```

### Invite Participants to the Channel

Once the group session is created, new participants can be invited
to join. Not all participants need to be added at the beginning;
you can add them later, even after communication has started.

```python
for invite in invites:
    invite_name = split_id(invite)
    await local_app.set_route(invite_name)
    handle = await created_session.invite(invite_name) # invite participant
    await handle   # awit for the invite to be finished
    print(f"{local} -> add {invite_name} to the group")
```

### Listen for New Sessions and Messages

Participants that need to join the group start without a session and wait to be
invited. To wait for an invitation, the application calls `listen_for_session`.
When an invite message is received, a new session is created at the SLIM session layer,
and `listen_for_session` returns the metadata for the newly created session.

```python
print_formatted_text("Waiting for session...", style=custom_style)
session = await local_app.listen_for_session()
```

When a new session is available, the participant can start listening for messages:

```python
while True:
    try:
        # Await next inbound message from the group session.
        # The returned parameters are a message context and the raw payload bytes.
        # Check session.py for details on MessageContext contents.
        ctx, payload = await session.get_message()
        print_formatted_text(
            f"{ctx.source_name} > {payload.decode()}",
            style=custom_style,
        )
    except asyncio.CancelledError:
        # Graceful shutdown path (ctrl-c or program exit).
        break
    except Exception as e:
        # Non-cancellation error; surface and exit the loop.
        print_formatted_text(f"-> Error receiving message: {e}")
        break
```

### Send Messages on a Channel

Each participant can also send messages at any time to the new session, and each message will be delivered to all participants connected to the same channel.

```python
# Send message to the channel_name specified when creating the session.
# As the session is group, all participants will receive it.
await shared_session_container[0].publish(user_input.encode())
```

## Creating Groups with the SLIM Controller

Another way to create a group in a SLIM network is to use the
[SLIM Controller](./slim-controller.md). For a complete description
on how to run it and the commands to use for the group creation and
management, please refer to the [Group Communication Tutorial](./slim-group-tutorial.md).
In this section, we list the `slimctl` commands to replicate
what we showed in the previous section.

### Create the Channel

First of all, you need to run the applications that you want to add to the group.
At that point, you can create the group by specifying the first participant in the
group. This will assign the role of moderator (like in the Python bindings examples),
but all the invites/removals will be done using the Controller and no action needs to be
performed in the application.

To create the group, run:

```bash
./slimctl controller channel create moderators=agntcy/ns/client-1/9494657801285491688
```

The outcome should be something similar to this:

```bash
Received response: agntcy/ns/xyIGhc2igNGmkeBDlZ
```

The name in the response is the name of the new channel created, with only one participant
added (e.g. `moderators=agntcy/ns/client-1/9494657801285491688`).

### Invite Participants to the Channel

Now that the channel is created, you can start to invite new participants. To do so, you can use
the following command:

```bash
./slimctl controller participant add -c agntcy/ns/xyIGhc2igNGmkeBDlZ agntcy/ns/client-2
```

The reply to the command should be similar to this:

```bash
Adding participant to channel ID agntcy/ns/xyIGhc2igNGmkeBDlZ: agntcy/ns/client-2
Participant added successfully to channel ID agntcy/ns/xyIGhc2igNGmkeBDlZ: agntcy/ns/client-2
```

Now the channel has two participants that can start to communicate
over the shared channel `agntcy/ns/xyIGhc2igNGmkeBDlZ`. Message reception and publishing
must be done within the application in the same way as shown in the previous section.
