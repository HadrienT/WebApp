from pydantic import BaseModel
from passlib.hash import bcrypt as bcrypt


class User(BaseModel):
    username: str
    email: str
    password: str


# Replace 'your_database_name' with your actual database name
def get_user(username: str, db):
    user = db.your_database_name.users.find_one({"username": username})
    if user:
        return User(**user)


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)
