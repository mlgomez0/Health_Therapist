import os
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), './../ml_models'))
sys.path.append(parent_dir)

from fastapi import FastAPI
from src.request import Request
from src.Phi3 import Phi3
from src.Rag import Rag
from fastapi.middleware.cors import CORSMiddleware

# Create an instance of the Phi3 and Rag classes
phi3 = Phi3()
rag = Rag()

# Create an instance of the FastAPI class
app = FastAPI()

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

    # Check if the model parameter is 'fine-tuned' or 'rag' and call the respective model
    response = ""
    if request.model == "fine-tuned":
        response = phi3.predict(request.conversation_id, request.text)
    elif request.model == "rag":
        response = rag.predict(request.conversation_id, request.text)
    else:
        response = "Invalid model parameter. Please use 'fine-tuned' or 'rag'."

    # Return the response
    return {
        "text": response
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