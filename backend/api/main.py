import os
import sys
import logging
from colorama import Fore, init
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.request import Request
#from src.Phi3 import Phi3
from src.Rag import Rag
from src.infraestructure.ConversationRepository import ConversationRepository
from src.infraestructure.DbContext import DbContext

logging.basicConfig(level=logging.INFO)

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './../ml_models'))
sys.path.append(parent_dir)

init(autoreset=True)

app = FastAPI()

origins = [
    "http://localhost:3000",  # React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#phi3 = Phi3()
rag = Rag()

conversation_repository = ConversationRepository(DbContext())

@app.get("/")
def read_root():
    return {
        "Module": "Capstone Project",
        "Author": "Group 2 - AIML",
        "Version": "0.0.1",
    }

@app.post("/api/chat")
def execute(request: Request):
    user_id = 1
    conversation_id = request.conversation_id
    if conversation_id <= 0:
        conversation_id = conversation_repository.create_conversation(user_id, request.model)

    response = ""
    if request.model == "fine-tuned":
        response = phi3.predict(conversation_id, request.text)
    elif request.model == "rag":
        response = rag.predict(conversation_id, request.text)
    else:
        response = "Invalid model parameter. Please use 'fine-tuned' or 'rag'."

    conversation_repository.create_message(conversation_id, request.text, response)

    return {
        "text": response,
        "conversation_id": conversation_id
    }

@app.get("/api/clear")
def clear_history():
    phi3.clear_history()
    return {
        "text": "Conversation history cleared"
    }

@app.get("/api/history")
def get_conversations():
    logging.info("Fetching conversation history...")
    user_id = 1  # Assuming a single user for simplicity
    result = conversation_repository.get_conversations(user_id)
    logging.info(f"History fetched: {result}")
    return result

@app.get("/api/conversation/{conversation_id}")
def get_conversation(conversation_id: int):
    logging.info(f"Fetching details for conversation ID: {conversation_id}")
    conversation = conversation_repository.get_conversation_by_id(conversation_id)
    if not conversation:
        logging.error(f"Conversation ID {conversation_id} not found.")
        raise HTTPException(status_code=404, detail="Conversation not found")
    logging.info(f"Details for conversation ID {conversation_id}: {conversation}")
    return conversation

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)
