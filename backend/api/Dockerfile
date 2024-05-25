FROM python:3.10-slim

COPY ./src ./app/src
COPY ./main.py /app
COPY ./requirements.txt /app
COPY ./start_service.sh /app

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["/bin/bash", "start_service.sh"]