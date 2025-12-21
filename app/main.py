from .api.controller import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import Database



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


@app.on_event("startup"):
async def on_startup():
    await Database.init_db()