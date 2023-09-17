from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from kv_database_be import handler
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
    return handler.get_statistics()

@app.get("/get-advice")
def get_adv():
    logger.info("Getting advice")
    return handler.get_advice()

@app.get("/get-avail-benchmarks")
def get_avail_bm():
    logger.info("Getting available benchmarks")
    return handler.get_avail_benchmarks()

@app.get("/get-avail-options")
def get_avail_opt():
    logger.info("Getting available options")
    return handler.get_avail_options()

@app.post("/upload-options-file/")
def upload_options_file(file: UploadFile):
    logger.info("Receiving options file")
    logger.info(f"File Name: {file.filename}")
    handler.create_options_file(file.file.read())
    return True