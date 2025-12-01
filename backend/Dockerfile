FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend ./backend
COPY data ./data

EXPOSE 5000
CMD ["python", "-m", "backend.api.tricount", "0.0.0.0"]
