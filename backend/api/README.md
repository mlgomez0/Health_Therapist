# Introduction

This capstone project allow users to interact with an AI LLM model.

## Installation

1. Create a Python virtual environment
```bash
python.exe -m venv .venv (Windows)
python3.10 -m venv .venv (MacOS)
```

2. Activate environment
```bash
.\.venv\Scripts\activate (Windows)
source .venv/bin/activate (MacOS)
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Set the following Env Variables

```bash

HF_API_TOKEN=XXXX
EMBEDDING_NAME=sentence-transformers/all-MiniLM-L6-v2
DATASET_PATH=backend/ml_models/datasets/dataset.csv
PERSIST_DIRECTORY=backend/api/chroma_db
CHROMA_DB_DIR=chroma_db
COLLECTION_NAME=mental_health_chats
PHI3_MODEL_NAME=microsoft/Phi-3-mini-4k-instruct
PHI3_BASE_MODEL_URL="" # model url in azure
AZURE_API_TOKEN=""
```

## Run service

To run the serive, follow the next steps:

1. Activate the Python environment
```bash
.\.venv\Scripts\activate (Windows)
source .venv/bin/activate (MacOS)
```

2. Run the command
```bash
uvicorn main:app --port 5000 --reload
```

If the latest command fails, try run the command `uvicorn main:app --port 5000`

## Use

**Request**

```http

POST /chat HTTP/1.1
Host: https://service-url
Content-Type: application/json

{
    "text": "Example text"
}

```

**Response**

```json
{
    "text": "This is a response"
}
```

## Create and publish Docker image

1. Create a Docker image
    ```bash
    docker build -t "captone-project-term3" . --tag=captone-project-term3:1.0.0
    ```

2. Create a container. The parameter -p has the format hostport:dockerport
    ```bash
    docker create --name=captone-project-term3 -p 5000:5000 captone-project-term3:1.0.0
    ```

3. Create a tag. You can change the version as needed
    ```bash
    docker tag captone-project-term3:1.0.0 dockername.azurecr.io/captone-project-term3:1.0.0
    ```
4. Push the image to Azure Container Registry
    ```bash
    az acr login --name dockername
    docker push dockername.azurecr.io/captone-project-term3:1.0.0
    ```


## Common issues

wsl --shutdown


## Database Configuration

### Create Database and Tables : Run the following commands to run the database

    ```bash
    python backend/api/database/setup_db.py <db_path>
    ```

### Method to create user and a conversation for testing

    ```bash
    python test_db.py <path_db> create_user <user_name>
    ```

    ```bash
    python test_db.py <path_db> create_conversation <user_id> <Context> <Answer>
    ```
## Setting up ChromaDB Vector Store

Run the following script:

    ```bash
    python backend/api/load_vectors/load_embeddings.py
    ```

For this script to run, you have to export the following env variables:

    ```bash
    export EMBEDDING_NAME="sentence-transformers/all-MiniLM-L6-v2"
    export DATASET_PATH="backend/ml_models/datasets/dataset.csv"
    export PERSIST_DIRECTORY="backend/api/chroma_db"
    export COLLECTION_NAME="mental_health_chats"
    ```


By runing the script with the above env vars, you will create a folder backend/chroma_db where the vectors DB files would be located



