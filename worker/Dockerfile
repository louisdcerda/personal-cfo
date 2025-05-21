FROM python:3.11-slim
WORKDIR /code

COPY ../backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY worker.py .
COPY backend ./backend


ENV PYTHONPATH="/code"
CMD ["python", "worker.py"]


