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