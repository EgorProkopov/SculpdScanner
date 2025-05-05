FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 7777

CMD ["uvicorn", "src.api.run:app", "--host", "0.0.0.0", "--port", "7777"]