FROM python:3.10-slim

# Instalar Git
RUN apt-get update && apt-get install -y git

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["/bin/bash", "start_service.sh"]
