from fastapi import FastAPI, HTTPException
from typing import List
from uuid import UUID,uuid4
from models import User, Gender, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id = uuid4(), 
        # uuid4 will generate differnt id's everytime when a change is made
        # id = UUID("c7f4334f-6fa8-4965-857b-20b47beb2c02"),
        # this will make the fixed id value and it will not change at any point
        first_name = "Max",
        last_name = "Well",
        gender = Gender.male,
        roles = [Role.student]

    ),
    User(
        # id = UUID("e5b5962f-ddc3-4566-b703-2d1e8cec5211"),
        id = uuid4(),
        first_name = "AB",
        last_name = "Devillers",
        gender = Gender.male,
        roles = [Role.admin, Role.user]

    )

]

@app.get("/")
async def test():
    return {"Hello": "Everyone"} 

@app.get("/api/v1/users")
async def fetch_users():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return 
    raise HTTPException(
        status_code=404,
        detail= f"user with id: {user_id} doesnot exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(status_code=404,
    details = f"user with id: {user_id} doesnot exists"
    )
