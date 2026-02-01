FROM python:3.14.2-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

CMD [ "uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]