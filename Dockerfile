FROM python:3.12-alpine

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    portaudio-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.enableCORS", "false"]
