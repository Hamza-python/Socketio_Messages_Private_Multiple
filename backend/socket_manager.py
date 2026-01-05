from datetime import datetime

# Store users and rooms (temporary memory)
connected_users = {}
rooms = {}

def register_socket_events(sio):

    @sio.event
    async def connect(sid, environ):
        print("Connected:", sid)

    @sio.event
    async def disconnect(sid):
        username = connected_users.get(sid)
        if username:
            del connected_users[sid]
        print("Disconnected:", sid)

    # 🔐 User login
    @sio.event
    async def join(sid, data):
        username = data["username"]
        connected_users[sid] = username

        await sio.emit(
            "user_list",
            list(connected_users.values())
        )

    # 💬 Private message
    @sio.event
    async def private_message(sid, data):
        receiver = data["to"]
        message = data["message"]

        for user_sid, username in connected_users.items():
            if username == receiver:
                await sio.emit(
                    "private_message",
                    {
                        "from": connected_users[sid],
                        "message": message,
                        "time": str(datetime.now())
                    },
                    to=user_sid
                )

    # 👥 Create / Join group
    @sio.event
    async def join_room(sid, data):
        room = data["room"]
        await sio.enter_room(sid, room)

    # 📢 Group message
    @sio.event
    async def group_message(sid, data):
        await sio.emit(
            "group_message",
            {
                "from": connected_users[sid],
                "room": data["room"],
                "message": data["message"],
                "time": str(datetime.now())
            },
            room=data["room"]
        )
