FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV STREAMLIT_WATCHDOG=none

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
