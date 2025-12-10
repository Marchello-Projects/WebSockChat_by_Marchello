import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status, HTTPException
from sqlalchemy.orm import Session

from app.managerWS import manager
from app.routes import auth_router
from app.routes.auth import get_user_from_token_ws_db 
from app.config.configdb import get_db

app = FastAPI(
    title="WebSockChat",
    description="Online chat using the WebSocket protocol",
    contact={
        "name": "Marchello",
        "url": "https://github.com/Marchello-Projects",
        "email": "paskalovmarkys@gmail.com",
    },
)

app.include_router(auth_router)


@app.websocket("/ws/chat")
async def chat(websocket: WebSocket, token: str):
    db: Session = next(get_db())
    try:
        user = await get_user_from_token_ws_db(token, db)
    except HTTPException:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user.username}: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", port=8000, reload=True)