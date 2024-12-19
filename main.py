from typing import Union

from fastapi import FastAPI

from crud.routes.routes_users import user

from config.db import conn

app = FastAPI()

app.include_router(user)
