from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from managerWS import manager
import uvicorn

app = FastAPI(
    title='WebSockChat',
    description='Online chat using the WebSocket protocol',
    contact={
        "name": "Marchello",
        "url": "https://github.com/Marchello-Projects",  
        "email": "paskalovmarkys@gmail.com"
    },
)

@app.websocket('/ws/chat')
async def chat(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(data, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == '__main__':
    uvicorn.run(f"{__name__}:app", port=8000, reload=True)