from fastapi import FastAPI
from dotenv import load_dotenv
import os
import subprocess

load_dotenv()
app = FastAPI()

db_dir = os.getenv("ROCKSDB_DIR")

@app.get("/live")
def live():
    return "I am alive"

@app.get("/test")
def test():
    command = [db_dir+"/db_bench",
                "--benchmarks=fillseq"]
    try:
        result = subprocess.run(command,capture_output=True,text=True,check=True)
        var_type = type(result.stdout)
        print(var_type)
        return result.stdout.split("\n")
    except subprocess.CalledProcessError as e:
        print(f"Error executing benchmark: {e}")
        print(e.stderr)