# SLIM Group Managment

One of the most important caracteristics of SLIM is that it allows secure group communincation.
A gruop in SLIM is a set of clients that can communicate together using a shared channel. The channel is
identified by a name, as described in [SLIM Messaging Layer](slim-data-plane.md). In addition, when MLS is
enable, the group communincation is protected by end-to-end encryption.

Here you will find all the information required to create a gruop
in a SLIM network.

 ## Gruop Creation Using a Moderator

 As descibe in [SLIM Messaging Layer](slim-data-plane.md), a gruop is managed by a moderator.
 A moderator is a particular client that is able to create a Channel, add and remove clients and performs the 
 functions delegeated to the delivery service by the MLS protocol.

 The moderator uses the SLIM python bindings in order to setup a group session and configure all the 
 required state to allow secure communication between participants. The moderator is part of a python application
 and it can be part of the communincation process implementing some logic, or it can be just used to moderate 
 the channel. A full example on how to use the moderator
 can be found in the [SLIM Group Communication Tutorial](slim-group-tutorila.md). Here we report the basic steps to follow
 with snipets of python code to setup a group.

- **Create the moderator**:  The moderator is created by creating a Streaming bidirectional session that
will create the corresponding state in the SLIM session layer. In this example the communication between 
partcipants will be encrypted end-to-end as MLS is enabled.

```python
    # Define the shared channel for group communication.
    # This channel will be used by all members of the group to exchange messages.
    shared_channel = PyName("agntcy", "namespace", "group_channel")

    # Create a new session. The group session is a bidirectional streaming session.
    # Here is where we enable the MLS protocol for end-to-end encryption.
    session_info = await slim_app.create_session(
        PySessionConfiguration.Streaming(
            PySessionDirection.BIDIRECTIONAL,
            topic=shared_channel,  # The channel ID for group communication.
            moderator=True,  # This session is created by the moderator.
            max_retries=5,  # Maximum number of retries for reliability.
            timeout=datetime.timedelta(seconds=5),  # Timeout for message delivery.
            mls_enabled=True,  # Enable MLS for end-to-end encryption.
        )
    )
```

-  **Invite Client to the Channel**:  Now the moderator needs to invite other partcipants to the 
channel. Notice that not all particpants needs to be added at the beginning but they can be add also later.

```python
    # Invite other members to the session.
    for invitee in invitees:
        print(f"Inviting {invitee}")
        await slim_app.set_route(invitee)  # Allow messages to be sent to the invitee.
        await slim_app.invite(
            session_info, invitee
        )  # Send an invitation to the invitee.
```

-  **The participants need to listen**: In other to receive the invitation to the channel each participant 
needs to listen for incoming messages. Notice the the invite message will be sent on the name of the particpant
and not on the channel as the partcipant doesn't know the channel yet

```python
    async with participant_slim_app:
        # Listen for new sessions opened by moderators
        recv_session, _ = await participant_slim_app.receive()

        # Session is received, now we can read and write on the shared channel.
        print(f"Received session: {recv_session.id}")

        # Receive messages from the session
        recv_session, msg_rcv = await participant_slim_app.receive(session=recv_session.id)

        # Print the message
        print(f"Received: {msg_rcv.decode()}")
```

At this point the group it set and the clients can start to exchange messages.
However this configuration is not reflected the SLIM Controller automatically and so it as to be reported manually
into the controller. In particular, if the SLIM network is composed by multiple nodes the registration to
the control plane is mandatory in order to properly setup the routes between nodes as the goup setup 
by the moderator itself can work out of the box only is a singlo SLIM node is present in the network.

In the next session we will describe out to register the new created group in the SLIM controller and 
how to properly set the routes between the nodes

## How to use the north bound control plane API

Laszlo - add commands for this part

- 1 create the group
- 2 add clients to the group
- 3 set the routes for the group name between slim nodes
 
 ## How to set idententity

 Muaro - spire example 