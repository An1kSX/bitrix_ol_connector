from .api.controller import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import database
from .db.models import *
from .bitrix.client import Bitrix



origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router, tags=["App Module"])


@app.on_event("startup")
async def on_startup():
    await database.init_db()

    portal = await db.get(Portal, "atbaccounting.bitrix24.kz")
    bx24 = Bitrix(portal)
    await bx24.get_users()
    