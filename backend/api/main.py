import os
import sys
from colorama import Fore, init

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './../ml_models'))
sys.path.append(parent_dir)

init(autoreset=True)

from fastapi import FastAPI,HTTPException
from src.request import Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.Phi3 import Phi3
from src.Rag import Rag
from fastapi.middleware.cors import CORSMiddleware
from src.infraestructure.ConversationRepository import ConversationRepository
from src.infraestructure.DbContext import DbContext
from src.infraestructure.UserRepository import UserRepository

# Create an instance of the Phi3 and Rag classes
phi3 = Phi3()
rag = Rag()

# Create an instance of the FastAPI class
app = FastAPI()
print(Fore.MAGENTA + "FastAPI app created")

# Create an instance of the ConversationRepository class
conversation_repository = ConversationRepository(DbContext())
user_repository = UserRepository(DbContext())
print(Fore.MAGENTA + "Database connected")

# Add CORS middleware to the FastAPI app
origins = [ "*" ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """
    Returns the metadata of the API
    """
    return {
        "Module": "Capstone Project",
        "Author": "Group 2 - AIML",
        "Version": "0.0.1",
    }


@app.post("/api/chat")
def execute(request: Request):
    """
    Returns the response of a user input using Phi3 model or Rag model based on the model parameter
    """

    # if the conversation_id is not provided, return an error message
    user_id = 1
    converstation_id = request.conversation_id
    if converstation_id <= 0:
        converstation_id = conversation_repository.create_conversation(user_id, request.model)

    # Check if the model parameter is 'fine-tuned' or 'rag' and call the respective model
    response = ""
    if request.model == "fine-tuned":
        response = phi3.predict(converstation_id, request.text)
    elif request.model == "rag":
        response = rag.predict(converstation_id, request.text)
    else:
        response = "Invalid model parameter. Please use 'fine-tuned' or 'rag'."

    # Return the response
    return {
        "text": response,
        "conversation_id": converstation_id
    }

@app.get("/api/clear")
def clear_history():
    """
    Clears the conversation history of the Phi3 model
    """
    phi3.clear_history()
    return {
        "text": "Conversation history cleared"
    }

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
