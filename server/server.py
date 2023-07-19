from fastapi import FastAPI, HTTPException
from gpt4all import GPT4All
from pydantic import BaseModel
import json

app = FastAPI()

processed_data = None

main_question = [
    'Create a JSON object based on the given sentence "',
    '" following this schema: "{subject: text, verb: text, object: text}". Consider the "subject" to represent the entity performing the action, the "verb" to represent the command, and the "object" to represent the target on which the action is being performed.'
]
gpt = GPT4All("GPT4All-13B-snoozy.ggmlv3.q4_0.bin", n_threads=28)


class InputDataRequest(BaseModel):
    command: str


def get_json(string):
    try:
        start_index = string.find("json") + len("json")
        end_index = string.find("```", start_index)
        json_string = string[start_index:end_index].strip()
        json_string = json_string.replace("'", "\"")
    except:
        # Se si verifica un errore, proviamo a trovare il JSON senza considerare il tag "json"
        start_index = string.find("{")
        end_index = string.find("}", start_index) + 1
        json_string = string[start_index:end_index].strip()
        json_string = json_string.replace("'", "\"")

    try:
        # Analizza la stringa JSON in un oggetto Python
        result = json.loads(json_string)
        return result
    except json.JSONDecodeError:
        return False


def process_data(data):
    result = gpt.generate(data)
    return get_json(result)


@app.post("/api/input_data/")
async def input_data(request: InputDataRequest):
    global processed_data
    processed_data = None
    processed_data = process_data(main_question[0] + request.command + main_question[1])
    return {"message": "Data received and processing started."}


@app.post("/api/check_status/")
async def check_status():
    global processed_data
    if processed_data is not None:
        return {"ready": True}
    else:
        return {"ready": False}


@app.post("/api/get_processed_data/")
async def get_processed_data():
    global processed_data
    if processed_data is not None:
        processed_data_temp = processed_data
        processed_data = None
        return processed_data_temp
    else:
        raise HTTPException(status_code=404, detail="Processed data not available yet.")
