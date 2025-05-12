from typing import Optional

from pydantic import BaseModel


class RoleInput(BaseModel):
    username: str
    role: str
    input_dialog: str


# 会话模型
class SessionInfo(BaseModel):
    session_id: Optional[str] = None


class TrainRoleInput(BaseModel):
    username: str
    custom_role: str
    user_input: Optional[str] = None
    iter_cnt: Optional[int] = 1