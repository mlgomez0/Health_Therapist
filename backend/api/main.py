from colorama import Fore, init
from fastapi import FastAPI, HTTPException, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.request import LlmRequest
from src.infraestructure.ConversationRepository import ConversationRepository
from src.infraestructure.DbContext import DbContext
from src.infraestructure.UserRepository import UserRepository
from src.Phi3 import Phi3
from src.Rag import Rag
import logging
import os
import sys

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

logging.basicConfig(level=logging.INFO)

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './../ml_models'))
sys.path.append(parent_dir)

init(autoreset=True)

# Create the Phi3 and Rag models
phi3 = Phi3()
rag = Rag()

# Create an instance of the FastAPI class
app = FastAPI()

origins = [
    "https://capstone-project-front-azfwc0gkdua0gpbr.eastus2-01.azurewebsites.net"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an instance of the ConversationRepository class
conversation_repository = ConversationRepository(DbContext())
user_repository = UserRepository(DbContext())
print(Fore.MAGENTA + "Database connected")

# Register router
router = APIRouter()

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
    logging.info(f"Existing user: {existing_user}")

    if not existing_user or existing_user['password'] != user.password:
        logging.error("Invalid username or password")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    logging.info("Login successful")
    return {"message": "Login successful", "user_id": existing_user['id']}

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
        phi3.clear_history()
        return {
            "text": "Conversation history cleared"
        }
    except Exception as e:
        logging.error(f"Error in /api/clear: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/api/history")
async def get_history(request: Request):
    user_id = request.headers.get('x-user-id')
    print("Hello",user_id)
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is required")
    
    result = conversation_repository.get_conversations(int(user_id))
    return result


@app.post("/api/chat")
async def chat(request: LlmRequest, http_request: Request):
    user_id = http_request.headers.get('x-user-id')
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID header is required")
    
    conversation_id = request.conversation_id
    model = request.model
    text = request.text

    if conversation_id <= 0:
        print(Fore.RED + "Creating new conversation")
        conversation_id = conversation_repository.create_conversation(int(user_id), model)
        print(Fore.GREEN + f"New conversation ID: {conversation_id}")

    response = ""
    summary = ""
    if model == "fine-tuned":
        response, summary = phi3.predict(conversation_id, text)
    elif model == "rag":
        response = rag.predict(conversation_id, text)
    else:
        response = "Invalid model parameter. Please use 'fine-tuned' or 'rag'."

    conversation_repository.create_message(conversation_id, text, response)

    response = {
        "text": response,
        "conversation_id": conversation_id,
        "summary": summary
    }

    print(Fore.GREEN + f"Response: {response}")
    return response

@app.get("/api/conversation/{conversation_id}")
def get_conversation(conversation_id: int):
    try:
        logging.info(f"Fetching details for conversation ID: {conversation_id}")
        conversation = conversation_repository.get_messages(conversation_id)
        if not conversation:
            logging.error(f"Conversation ID {conversation_id} not found.")
            raise HTTPException(status_code=404, detail="Conversation not found")
        logging.info(f"Details for conversation ID {conversation_id}: {conversation}")
        return conversation
    except Exception as e:
        logging.error(f"Error in /api/conversation/{conversation_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/feedback")
async def submit_feedback(feedback: Feedback, request: Request):
    username = request.headers.get('x-username')
    if not username:
        raise HTTPException(status_code=400, detail="Username header is required")
    
    user = user_repository.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    conversation_repository.update_feedback(feedback.conversation_id, feedback.user_score, feedback.user_feedback)
    return {"message": "Feedback submitted successfully"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)
