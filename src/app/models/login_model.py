from pydantic import BaseModel


class LoginForm(BaseModel):
    email: str
    password: str
    remember_me: bool
