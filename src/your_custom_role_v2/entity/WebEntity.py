from pydantic import BaseModel


class RoleInput(BaseModel):
    username: str
    role: str
    input_dialog: str
