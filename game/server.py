import socketio
from fastapi import FastAPI

sio = socketio.AsyncServer(async_mode='asgi')
app = FastAPI()

app.mount("/", socketio.ASGIApp(sio))

@sio.on("connect")
async def connect(sid, environ, auth):
    print("A connection was made from", sid)

@sio.on("disconnect")
async def disconnect(sid):
    print(sid, "has disconnected")

