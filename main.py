from typing import List
from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4

from models import Gender, User, Role, UserUpdateRequest

app = FastAPI()


db: List[User] = [
    User(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        email="asd@as.com",
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    ),
    User(
        id=uuid4(),
        first_name="Jane",
        last_name="Doe",
        middle_name="Smith",
        email="dd@a.com",
        gender=Gender.female,
        roles=[Role.student]
    )
]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get('/api/v1/users')
async def get_users():
    return db


@app.post('/api/v1/users')
async def create_user(user: User):
    db.append(user)
    return user


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User id {user_id} not found")


@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user: UserUpdateRequest):
    for db_user in db:
        if db_user.id == user_id:
            if user.first_name:
                db_user.first_name = user.first_name
            if user.last_name:
                db_user.last_name = user.last_name
            if user.middle_name:
                db_user.middle_name = user.middle_name
            if user.roles:
                db_user.roles = user.roles
            return {"message": "User updated successfully"}
    raise HTTPException(status_code=404, detail=f"User id {user_id} not found")
