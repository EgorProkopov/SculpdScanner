FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update \
    && apt-get install -y libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY src/ ./src/

EXPOSE 8888

CMD ["uvicorn", "src.api.run:app", "--host", "0.0.0.0", "--port", "8888"]
