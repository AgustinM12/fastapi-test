from typing import Union

from fastapi import FastAPI

from crud.routes.routes_users import user

from config.db import conn

app = FastAPI(
    title="TEST FASTPI - MONGODB",
    description="Prueba para usar el framework de fastApi")


# TODO: AÑADIR PREFIJO A LAS RUTAS
app.include_router(prefix="/api", router=user)
