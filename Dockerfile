FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
RUN apt-get update && apt-get upgrade -y
COPY ./app /app
RUN pip install -r requirements.txt
# additional to load spacy models
RUN python -m spacy download en_core_web_sm