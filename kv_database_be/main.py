from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from kv_database_be.handlers import h_common, h_statistics, h_advice
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

@app.get("/get-avail-benchmarks")
def get_avail_bm():
    logger.info("Getting available benchmarks")
    return h_common.get_avail_benchmarks()

@app.post("/upload-options-file")
def upload_options_file(file: UploadFile):
    logger.info("Receiving options file")
    logger.info(f"File Name: {file.filename}")
    return h_common.create_options_file(file.file.read())

@app.get("/get-statistics")
def get_stats(benchmark: str):
    logger.info("Getting statistics "+benchmark)
    return h_statistics.get_statistics(benchmark)

@app.get("/get-advice")
def get_adv(db_path: str):
    logger.info("Getting advice from "+db_path)
    return h_advice.get_advice(db_path)