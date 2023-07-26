from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from kv_database_be.handler import get_statistics
from kv_database_be.log import logger

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/live")
def live():
    return "I am alive"

@app.get("/get-statistics")
def get_stats():
    logger.info("Getting statistics")
    return get_statistics()