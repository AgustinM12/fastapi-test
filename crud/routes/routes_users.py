from fastapi import APIRouter, Response, status
from crud.schemas.user_entity import userEntity, usersEntity
from config.db import conn
from crud.models.model_user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()


@user.get("/test")
def helloworld():
    return "hello world!"


@user.get("/users", response_model=list[User], tags=["users"])
def find_all_users():
    return usersEntity(conn.local.user.find())


@user.get("/user/{id}", tags=["users"])
def find_user(id: str):
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@user.post("/user", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])

    id = conn.local.user.insert_one(new_user).inserted_id

    created_user = conn.local.user.find_one({"_id": id})

    return userEntity(created_user)


@user.put("/user/{id}", tags=["users"])
def update_user(id: str, user: User):
    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


@user.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(id: str):
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
