import os
import sys
import logging
from colorama import Fore, init
from fastapi import FastAPI, HTTPException, APIRouter, Request  # Ensure Request is imported
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from src.infraestructure.ConversationRepository import ConversationRepository
from src.infraestructure.DbContext import DbContext
from src.infraestructure.UserRepository import UserRepository
from src.Rag import Rag  # Ensure Rag is imported correctly

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

rag = Rag()
conversation_repository = ConversationRepository(DbContext())

# Register router
router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str

class Feedback(BaseModel):
    conversation_id: int
    user_score: int
    user_feedback: str

db_context = DbContext()
user_repository = UserRepository(db_context)

@router.post("/api/register")
async def register_user(user: UserRegister):
    existing_user = user_repository.get_user_by_username_or_email(user.username, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    user_repository.create_user(user.username, user.email, user.password)
    return {"message": "Registration successful"}

@router.post("/api/login")
async def login_user(user: UserLogin):
    logging.info(f"Login attempt for username: {user.username}")
    existing_user = user_repository.get_user_by_username(user.username)
    if existing_user is None or existing_user['password'] != user.password:
        logging.error("Invalid username or password")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    logging.info("Login successful")
    return {"message": "Login successful"}

@router.post("/api/feedback")
async def submit_feedback(feedback: Feedback, request: Request):
    username = request.headers.get('x-username')
    if not username:
        raise HTTPException(status_code=400, detail="Username header is required")
    
    user = user_repository.get_user_by_username(username)
    print(username)
    print(feedback)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    conversation_repository.update_feedback(feedback.conversation_id, feedback.user_score, feedback.user_feedback)
    return {"message": "Feedback submitted successfully"}

app.include_router(router)

@app.get("/")
def read_root():
    return {
        "Module": "Capstone Project",
        "Author": "Group 2 - AIML",
        "Version": "0.0.1",
    }

@app.get("/api/clear")
def clear_history():
    try:
        return {
            "text": "Conversation history cleared"
        }
    except Exception as e:
        logging.error(f"Error in /api/clear: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/history")
async def get_history():
    user_id = 1  # Assuming a single user for simplicity
    result = conversation_repository.get_conversations(user_id)
    return result

@app.post("/api/chat")
async def chat(request: Request):  # Ensure request is of type Request
    user_id = 1
    conversation_id = request.conversation_id
    model = request.model
    text = request.text

    if conversation_id <= 0:
        conversation_id = conversation_repository.create_conversation(user_id, model)

    response = rag.predict(conversation_id, text)
    conversation_repository.create_message(conversation_id, text, response)
    return {"text": response, "conversation_id": conversation_id}

@app.get("/api/conversation/{conversation_id}")
def get_conversation(conversation_id: int):
    try:
        logging.info(f"Fetching details for conversation ID: {conversation_id}")
        conversation = conversation_repository.get_conversation_by_id(conversation_id)
        if not conversation:
            logging.error(f"Conversation ID {conversation_id} not found.")
            raise HTTPException(status_code=404, detail="Conversation not found")
        logging.info(f"Details for conversation ID {conversation_id}: {conversation}")
        return conversation
    except Exception as e:
        logging.error(f"Error in /api/conversation/{conversation_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)
