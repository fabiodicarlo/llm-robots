from fastapi import FastAPI, HTTPException
from gpt4all import GPT4All
import re
import json

app = FastAPI()

processed_data = None
gpt = GPT4All("ggml-wizardLM-7B.q4_2.bin", n_threads=28)


def get_json(string):
    match = re.search(r'json\s*{(.+?)}', string, re.DOTALL | re.IGNORECASE)
    if not match:
        return False

    extracted_json = match.group(1)
    fixed_json = re.sub(r"(\w+):", r'"\1":', extracted_json.replace("'", '"'))

    try:
        json.loads(fixed_json)
        return True
    except json.JSONDecodeError:
        return False


def process_data(data):
    result = gpt.generate(data)
    return get_json(result)


@app.post("api/input_data/")
async def input_data(request: str):
    global processed_data
    processed_data = None
    processed_data = process_data(request)
    return {"message": "Data received and processing started."}


@app.post("api/check_status/")
async def check_status():
    global processed_data
    if processed_data is not None:
        return {"ready": True}
    else:
        return {"ready": False}


@app.post("api/get_processed_data/")
async def get_processed_data():
    global processed_data
    if processed_data is not None:
        processed_data = None
        return processed_data
    else:
        raise HTTPException(status_code=404, detail="Processed data not available yet.")
