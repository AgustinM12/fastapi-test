from fastapi import APIRouter
from crud.schemas.user_entity import userEntity, usersEntity
from config.db import conn
from crud.models.model_user import User
from passlib.hash import sha256_crypt

user = APIRouter()

@user.get("/test")
def helloworld():
    return "hello world!"


@user.get("/users")
def find_all_users():   
    return usersEntity(conn.local.user.find())


@user.get("/user/{id}")
def find_user():   
    return ""

@user.post("/user")
def create_user(user: User):   
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])  
    
    id = conn.local.user.insert_one(new_user).inserted_id
    
    created_user = conn.local.user.find_one({"_id":id})
    
    return userEntity(created_user)

@user.put("/user/{id}")
def update_user():   
    return ""

@user.delete("/user/{id}")
def delete_user():   
    return ""
