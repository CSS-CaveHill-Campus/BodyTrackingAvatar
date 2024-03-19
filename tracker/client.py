import socketio
from time import sleep

client = socketio.SimpleClient()
client.connect("http://localhost:8000")

    