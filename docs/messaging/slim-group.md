# SLIM Group Creation

One of the key features of [SLIM](slim-core.md) is its support for secure group communication.
In SLIM, a group consists of multiple clients that communicate through a shared
channel. Each channel is identified by a unique name, as described in the [SLIM
Messaging Layer](slim-data-plane.md). When MLS is enabled, group
communication benefits from end-to-end encryption.

This guide provides all the information you need to create and manage groups within a
SLIM network.

## Creating Groups with the Python Bindings


This section shows how to use the SLIM Python bindings to create a group.
This requires a [multicast session](./slim-session.md#multicast). A multicast
session is a channel shared among multiple participants and used to
send messages to everyone. When a new participant wants to join the channel,
they must be invited by the channel creator.

The channel creator can be part of a Python application and can either
actively participate in the communication process (possibly implementing some
of the application logic) or serve solely as a channel moderator. For a complete
example of how to use the moderator, see the [SLIM Group
Communication Tutorial](slim-group-tutorial.md).

This section provides the basic
steps to follow, along with Python code snippets, for setting up a multicast session.
A complete [example](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/multicast.py) of group communication can be found in the SLIM repo, in addition
to a related [README](https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/examples/src/slim_bindings_examples/README_multicast.md) with explanations on how to run it.

### Create the Channel

The channel can be created by instantiating a Multicast session,
which initializes the corresponding state in the SLIM session layer.
In this example, communication between participants will be encrypted
end-to-end, as MLS is enabled.

```python
created_session = await local_app.create_session(
    slim_bindings.PySessionConfiguration.Multicast(  # type: ignore  # Build multicast session configuration
        channel_name=chat_channel,  # Logical multicast channel (PyName) all participants join; acts as group/topic identifier.
        max_retries=5,  # Max per-message resend attempts upon missing ack before reporting a delivery failure.
        timeout=datetime.timedelta(
            seconds=5
        ),  # Ack / delivery wait window; after this duration a retry is triggered (until max_retries).
        mls_enabled=enable_mls,  # Enable Messaging Layer Security for end-to-end encrypted & authenticated group communication.
    )
)
```

### Invite Participants to the Channel

Once the multicast session is created, new participants can be invited
to join. Not all participants need to be
added initially; you can add them later, even after communication
has already started.

```python
# Invite each provided participant. Route is set before inviting to ensure
# outbound control messages can reach them. For more info see
# https://github.com/agntcy/slim/blob/main/data-plane/python/bindings/SESSION.md#invite-a-new-participant
for invite in invites:
    invite_name = split_id(invite)
    await local_app.set_route(invite_name)
    await created_session.invite(invite_name)
    print(f"{local} -> add {invite_name} to the group")
```

### Listen for Invitations and Messages

Participants that need to join the group start without a session and wait to be
invited. To wait for an invitation, the application calls `listen_for_session`.
When an invite message is received, a new session is created at the SLIM session layer,
and `listen_for_session` returns the metadata for the newly created session.

```python
format_message_print(local, "-> Waiting for session...")
session = await local_app.listen_for_session()
```


At this point, when a session is available, the participant can start listening for messages:

```python
while True:
    try:
        # Await next inbound message from the multicast session.
        # The returned parameters are a message context and the raw payload bytes.
        # Check session.py for details on PyMessageContext contents.
        ctx, payload = await session.get_message()
        format_message_print(
            local,
            f"-> Received message from {ctx.source_name}: {payload.decode()}",
        )
    except asyncio.CancelledError:
        # Graceful shutdown path (ctrl-c or program exit).
        break
    except Exception as e:
        # Non-cancellation error; surface and exit the loop.
        format_message_print(local, f"-> Error receiving message: {e}")
        break
```

The next section describes how to register the newly created group
with the SLIM Controller and configure routes between nodes.

## Creating Groups with the SLIM Controller

The controller API exposes operations to manage SLIM groups. You can use this API in client
applications to create and manage SLIM groups, add clients to
groups, and set routes between SLIM nodes.

You can generate gRPC API SDKs from the [schema
registry](https://buf.build/agntcy/slim/sdks/main:protobuf).

The following sections show example Python code fragments:

### Creating a SLIM Channel

```python
import grpc
from controlplane.v1 import controlplane_pb2_grpc as controlplane_api
from controlplane.v1 import controlplane_pb2

# Create gRPC connection
channel = grpc.insecure_channel("localhost:50051")
client = controlplane_api.ControlPlaneServiceStub(channel)

# Create channel request
create_channel_request = controlplane_pb2.CreateChannelRequest(
    moderators=["agntcy/namespace/moderator"]  # Name of the moderator
)

try:
    response = client.CreateChannel(create_channel_request)
    channel_id = response.channel_id

    if not response:
        print("\nNo channels found")
        return

    print(f"Channel created with ID: {channel_id}")

except grpc.RpcError as e:
    print(f"Request failed: {e}")
finally:
    channel.close()
```

### Adding Participants to a SLIM Group

```python
import grpc
from controlplane.v1 import controlplane_pb2_grpc as controlplane_api
from controlplane.v1 import controlplane_pb2

# Create gRPC connection
channel = grpc.insecure_channel("localhost:50051")
client = controlplane_api.ControlPlaneServiceStub(channel)

# Add participant request
add_participant_request = controlplane_pb2.AddParticipantRequest(
    participant_id="agntcy/namespace/participant_1",
    channel_id="agntcy/namespace/group_channel"
)

try:
    ack = client.AddParticipant(add_participant_request)

    print(f"ACK received for {ack.original_message_id}: success={ack.success}")

except grpc.RpcError as e:
    print(f"Request failed: {e}")
finally:
    channel.close()
```

### Setting Routes Between SLIM Nodes

```python
import grpc
from controlplane.v1 import controlplane_pb2_grpc as controlplane_api
from controlplane.v1 import controlplane_pb2
from grpc_api import grpc_api_pb2 as grpcapi

# Create gRPC connection
channel = grpc.insecure_channel("localhost:50051")
client = controlplane_api.ControlPlaneServiceStub(channel)

try:
    # Create connection to the target node
    connection = grpcapi.Connection(
        connection_id="http://127.0.0.1:46357",
        config_data='{"endpoint": "http://127.0.0.1:46357"}'
    )

    create_connection_request = controlplane_pb2.CreateConnectionRequest(
        connection=connection,
        node_id="slim/0"
    )

    create_connection_response = client.CreateConnection(create_connection_request)

    if not create_connection_response.success:
        raise Exception("Failed to create connection")

    connection_id = create_connection_response.connection_id
    print(f"Connection created successfully with ID: {connection_id}")

    # Add subscription for a group to a SLIM node
    subscription = grpcapi.Subscription(
        component_0="agntcy",
        component_1="namespace",
        component_2="group_channel",
        connection_id=connection_id
    )

    create_subscription_request = controlplane_pb2.CreateSubscriptionRequest(
        node_id="slim/0",
        subscription=subscription
    )

    create_subscription_response = client.CreateSubscription(create_subscription_request)

    if not create_subscription_response.success:
        raise Exception("Failed to create subscription")

    print(f"Subscription created successfully with ID: {create_subscription_response.subscription_id}")

except grpc.RpcError as e:
    print(f"gRPC error: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    channel.close()
```
