from typing import List, Dict
from datetime import datetime, timedelta
from app.database.models import UserRole
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        try:
            await websocket.send_text(message)
        except:
            pass  

    async def broadcast(self, message: str, sender: WebSocket | None = None):
        for connection in self.active_connections[:]: 
            if connection != sender:
                try:
                    await connection.send_text(message)
                except:
                    self.active_connections.remove(connection)


class ModerationManager:
    def __init__(self):
        self.banned_users: set[str] = set()  
        self.muted_users: Dict[str, datetime] = {} 
        self.forbidden_words: List[str] = ["badword1", "badword2"]
        self.logs: List[str] = []

    def _normalize_username(self, username: str) -> str:
        """Приводим имя к единому виду: нижний регистр + убираем пробелы по краям"""
        return username.strip().lower()

    def check_permissions(self, user_role: str, required_role: str) -> bool:
        roles_order = [
            UserRole.USER.value,
            UserRole.MODERATOR.value,
            UserRole.ADMIN.value
        ]
        return roles_order.index(user_role) >= roles_order.index(required_role)

    def parse_command(self, command: str, target_raw: str, issuer_user) -> str:
        action = command.lower()
        now = datetime.now()
        target = self._normalize_username(target_raw)

        if action == "/kick":
            if not self.check_permissions(issuer_user.role, UserRole.MODERATOR.value):
                return "No permission to kick"
            self.logs.append(f"{now} - {issuer_user.username} kicked {target_raw}")
            return f"User {target_raw} kicked"

        if action == "/ban":
            if not self.check_permissions(issuer_user.role, UserRole.MODERATOR.value):
                return "No permission to ban"
            self.banned_users.add(target)
            self.logs.append(f"{now} - {issuer_user.username} banned {target_raw}")
            return f"User {target_raw} banned"

        if action == "/mute":
            if not self.check_permissions(issuer_user.role, UserRole.MODERATOR.value):
                return "No permission to mute"
            mute_until = now + timedelta(minutes=5)
            self.muted_users[target] = mute_until
            self.logs.append(f"{now} - {issuer_user.username} muted {target_raw} until {mute_until}")
            return f"User {target_raw} muted until {mute_until:%Y-%m-%d %H:%M:%S}"

        if action == "/warn":
            if not self.check_permissions(issuer_user.role, UserRole.MODERATOR.value):
                return "No permission to warn"
            self.logs.append(f"{now} - {issuer_user.username} warned {target_raw}")
            return f"User {target_raw} warned"

        return "Unknown command"

    def filter_message(self, message: str) -> str:
        words = message.split()
        for i, word in enumerate(words):
            if word.lower() in self.forbidden_words:
                words[i] = "*" * len(word)
        return " ".join(words)

    def is_muted(self, username: str) -> bool:
        norm_username = self._normalize_username(username)
        mute_end = self.muted_users.get(norm_username)

        if mute_end:
            if datetime.now() < mute_end:
                return True
            else:
                self.muted_users.pop(norm_username, None)
        return False

    def is_banned(self, username: str) -> bool:
        return self._normalize_username(username) in self.banned_users


manager = ConnectionManager()
moderation = ModerationManager()  