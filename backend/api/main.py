from colorama import Fore, init
from fastapi import FastAPI, HTTPException, APIRouter  # Ensure Request is imported
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.infraestructure.ConversationRepository import ConversationRepository
from src.infraestructure.DbContext import DbContext
from src.infraestructure.UserRepository import UserRepository
from src.Phi3 import Phi3
from src.Rag import Rag
from src.request import Request
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
    os.getenv("ALLOW_ORIGINS") # "http://localhost:3000"
]
# Create an instance of the ConversationRepository class
conversation_repository = ConversationRepository(DbContext())
user_repository = UserRepository(DbContext())
print(Fore.MAGENTA + "Database connected")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    if existing_user == None or existing_user['password'] != user.password:  # Ensure the index is correct for password
        logging.error("Invalid username or password")
        raise HTTPException(status_code=401, detail="Invalid username or password")

    logging.info("Login successful")
    return {"message": "Login successful"}

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
        print(Fore.RED + "Creating new conversation")
        conversation_id = conversation_repository.create_conversation(user_id, model)
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

@app.get("/api/history")
def get_conversations():
    """
    Returns the conversations history
    """
    user_id = 1
    result = conversation_repository.get_conversations(user_id)
    return result

# User management API models and endpoints
class User(BaseModel):
    username: str
    password: str

@app.post("/users/")
def create_user(user: User):
    user_id = user_repository.insert_user(user.username, user.password)
    if user_id:
        return {"id": user_id, "username": user.username}
    else:
        raise HTTPException(status_code=400, detail="User creation failed")

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    rows_affected = user_repository.update_user(user_id, user.username, user.password)
    if rows_affected:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    rows_affected = user_repository.delete_user(user_id)
    if rows_affected:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/api/feedback")
async def submit_feedback(feedback: Feedback):
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

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)
