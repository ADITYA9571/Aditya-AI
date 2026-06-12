"""Week-3 assignment"""
import json
from typing import Annotated, Optional
import tiktoken
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

class TextToken(BaseModel):
    text : str
    model : str

class TaskAssignment(BaseModel):
    weekly_tasks_id: str
    tasks: str

class TaskUpdate(BaseModel):
    weekly_tasks_id: str
    tasks: Annotated[Optional[str],Field(default=None)]

def load_data():
    with open('weekly_tasks.json', 'r', encoding="utf-8") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('weekly_tasks.json','w', encoding="utf-8") as f:
        json.dump(data,f)

MODEL_COSTS = {
    "gpt-5": 1.25,
    "gpt-5-mini": 0.25,
    "gpt-5-nano": 0.05,
    "gpt-4.1": 2.00,
    "gpt-4.1-mini": 0.40,
    "gpt-4.1-nano": 0.10,
    "gpt-4o": 2.50,
    "gpt-3.5-turbo": 0.50,
}

def token_counter(str1:str, model:str):
    if model not in MODEL_COSTS:
        raise HTTPException(status_code=400, detail='Unsupported model')
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(str1)
    token_count = len(tokens)
    char_count = len(str1)
    word_count = len(str1.split())
    input_cost = (token_count / 1_000_000) * MODEL_COSTS[model]
    return {"model": model,
            "rate": f"${MODEL_COSTS[model]}/1M tokens",
            "characters": char_count,
            "words": word_count,
            "tokens": token_count,
            "input_cost": round(input_cost, 7)}

@app.get("/")
def hello():
    return {'message':'Token Counter'}

@app.get('/about')
def about():
    return {'message':'API deployment for token counter'}

@app.post('/text-tokens')
async def text_tokens(data: TextToken):
    return token_counter(data.text, data.model)

@app.post('/file-tokens')
async def file_tokens(file: UploadFile = File(...),model: str = "gpt-5"):
    try:
        content = await file.read()
        text = content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400,detail="Only UTF-8 text files are supported") from exc
    return token_counter(text, model)

@app.post('/create')
async def add_task(task_assign:TaskAssignment):
    weekly_tasks = load_data()
    if task_assign.weekly_tasks_id in weekly_tasks:
        raise HTTPException(status_code=404,detail="Task already assigned")
    weekly_tasks[task_assign.weekly_tasks_id] = {"tasks": task_assign.tasks}
    save_data(weekly_tasks)
    return {"message": "Task created successfully",
            "task": weekly_tasks[task_assign.weekly_tasks_id]}

@app.get("/weekly_tasks/{weekly_tasks_id}")
async def get_sample(weekly_tasks_id: str):
    weekly_tasks = load_data()
    if weekly_tasks_id not in weekly_tasks:
        raise HTTPException(status_code=404,detail="Task not found")
    return weekly_tasks[weekly_tasks_id]

@app.get("/weekly_tasks")
async def get_all_tasks():
    return load_data()

@app.put("/update")
async def update(task_update: TaskUpdate):
    data = load_data()
    task_id = task_update.weekly_tasks_id

    if task_id not in data:
        raise HTTPException(status_code=404,detail="Task id not found")

    if task_update.tasks is not None:
        data[task_id]["tasks"] = task_update.tasks

    save_data(data)
    return JSONResponse(status_code=200,content={"message": "Data updated successfully"})

@app.delete('/delete/{weekly_tasks_id}')
def delete_task(weekly_tasks_id: str):
    data = load_data()
    if weekly_tasks_id not in data:
        raise HTTPException(status_code=404, detail='Task doesnt exists')
    del data[weekly_tasks_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':'Task Deleted'})
