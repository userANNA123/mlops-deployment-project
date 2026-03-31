FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY scripts ./scripts
COPY artifacts ./artifacts
COPY data ./data

EXPOSE 7860

 # CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
 CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
