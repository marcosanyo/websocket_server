import asyncio
import uvicorn
from fastapi import FastAPI, WebSocket
from typing import Set


app = FastAPI()
connected: Set[WebSocket] = set()
user_count = 0

async def notify_users(message, sender_name):
    if connected:  # 接続中のユーザーがいる場合
        await asyncio.wait([user.send_text(f"{sender_name}: {message}") for user in connected])
        print(f"Message sent to connected users: {sender_name}: {message}")

async def increment_user_count():
    global user_count
    user_count += 1
    return f"User{user_count}"

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected.add(websocket)
    user = await increment_user_count()
    await websocket.send_text(f"Welcome, {user}!")
    print(f"{user} joined the chat")
    await notify_users(f"{user} joined the chat", "Server")
    print(f"Connected users: {len(connected)}")
    try:
        while True:
            data = await websocket.receive_text()
            await notify_users(data, f"User{user_count}")
    except:
        connected.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
