FROM python:3.10-slim

# Set environment variables
ENV PHI3_BASE_MODEL_URL="https://phi-3-small-128k-instruct-nribc.eastus2.models.ai.azure.com/chat/completions"
ENV FINE_TUNED_MODEL_URL="https://phi-3-mental-health.eastus2.models.ai.azure.com/chat/completions"
ENV BASE_MODEL_API_KEY="CVIYBRXOy5Rtc9ED6RhEME4EtXg245v6"
ENV FINE_TUNED_MODEL_API_KEY="SX9pxcbMic9DdOGMBBg7MCUtYXpPpwnk"
ENV HF_API_TOKEN="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"
ENV EMBEDDING_NAME="sentence-transformers/all-MiniLM-L6-v2"
ENV DATASET_PATH="backend/ml_models/datasets/dataset.csv"
ENV PERSIST_DIRECTORY="backend/api/chroma_db"
ENV COLLECTION_NAME="mental_health_chats"
ENV ALLOW_ORIGINS="https://capstone-project-front-azfwc0gkdua0gpbr.eastus2-01.azurewebsites.net"
ENV CHROMA_DB_DIR="chroma_db"

# Instalar Git
RUN apt-get update && apt-get install -y git

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["/bin/bash", "start_service.sh"]
