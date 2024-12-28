from fastapi import APIRouter, Response, status, Path, Query
from crud.schemas.user_entity import userEntity, usersEntity
from config.db import conn
from crud.models.model_user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

# TODO: TIPO DE RESPUESTAS QUE PUEDE TENER FAST API
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
    JSONResponse,
    PlainTextResponse,
    StreamingResponse,
    RedirectResponse,
)

user = APIRouter()


# TODO: RUTA DE EJEMPLO Y EJEMPLO DE COMO INDICAR QUE SE VA A RETORNAR EN UNA FUNCION
@user.get("/test")
def helloworld() -> str:
    return "hello world!"


@user.get("/users", response_model=list[User], tags=["users"])
def find_all_users():
    return usersEntity(conn.local.user.find())


# TODO: EJEMPLO DE PARAMETROS DE RUTA
# TODO: EJEMPLO DE VALIDACION DE PARAMETROS, PATH VALIDA LOS DATOS RECIBIDOS
# TODO: EJEMPLO DE VALIDACION DE DEVOLUCIONES
@user.get("/user/{id}", tags=["users"])
def find_user(id: str = Path(gt=0)) -> userEntity | None:
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


# TODO: EJEMPLOS DE PARAMETROS QUERY, SE DEBEN AGREGAR VARIABLES A LAS FUNCIONES
#TODO: EJEMPLO DE STATUS CODE
@user.post("/user", response_model=User, tags=["users"])
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])

    id = conn.local.user.insert_one(new_user).inserted_id

    created_user = conn.local.user.find_one({"_id": id})

    return JSONResponse(content=userEntity(created_user), status_code=201)



@user.put("/user/{id}", tags=["users"])
def update_user(id: str, user: User):
    conn.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(conn.local.user.find_one({"_id": ObjectId(id)}))


# TODO: VALIDACION DE QUERY
# TODO: EJEMPLO DE COLOCAR CODIGOS DE ESTADO ESPERADOS
@user.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"], response_description="En caso de salir bien se devuelve status 204, ejemplo de descripcion para las respuestas")
def delete_user(id: str = Query(gt=0)) -> None:
    userEntity(conn.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
