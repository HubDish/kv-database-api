from fastapi import FastAPI
from kv_database_be.handler import get_statistics
from kv_database_be.log import logger

app = FastAPI()

@app.get("/live")
def live():
    return "I am alive"

@app.get("/get-statistics")
def get_stats():
    logger.info("Getting statistics")
    return get_statistics()