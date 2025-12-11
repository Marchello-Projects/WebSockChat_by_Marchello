import uvicorn
from fastapi import (FastAPI, HTTPException, WebSocket, WebSocketDisconnect,
                     status)
from sqlalchemy.orm import Session

from app.config.configdb import get_db
from app.managerWS import manager, moderation
from app.routes import auth_router
from app.routes.auth import get_user_from_token_ws_db

app = FastAPI(
    title="WebSockChat",
    description="Online chat using the WebSocket protocol",
    # year.month.day.major.minor
    version="25.12.10.1.1",
    contact={
        "name": "Marchello",
        "url": "https://github.com/Marchello-Projects",
        "email": "paskalovmarkus@gmail.com",
    }
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

    if moderation.is_banned(user.username):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            if data.startswith("/"):
                parts = data.split(maxsplit=1)
                command = parts[0]
                target = parts[1] if len(parts) > 1 else ""
                response = moderation.parse_command(command, target, user)
                await manager.send_personal_message(response, websocket)
                continue

            if moderation.is_muted(user.username):
                await manager.send_personal_message("You are muted", websocket)
                continue

            filtered_message = moderation.filter_message(data)
            await manager.broadcast(f"{user.username}: {filtered_message}", websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)
