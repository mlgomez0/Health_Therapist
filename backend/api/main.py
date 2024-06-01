import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './../ml_models'))
sys.path.append(parent_dir)

from first_model import ResponseGenerator
from chat_model1 import ChatModel1
from fastapi import FastAPI
from src.request import Request
from fastapi.middleware.cors import CORSMiddleware


model = ResponseGenerator()
#model = ChatModel1()

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "Module": "Capstone Project",
        "Author": "Group 2 - AIML",
        "Version": "0.0.1",
    }


class Item():
    name: str

@app.post("/api/chat")
def execute(request: Request):
    response = model.generate_response(request.text)
    return {
        "text": response
    }