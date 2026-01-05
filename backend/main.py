import socketio
from fastapi import FastAPI
from socket_manager import register_socket_events

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*"
)

app = FastAPI()
socket_app = socketio.ASGIApp(sio, app)

register_socket_events(sio)

@app.get("/")
def root():
    return {"status": "Chat server running"}
