
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python -m textblob.download_corpora


COPY . .


EXPOSE 8501


CMD ["streamlit", "run", "app.py", "--server.port=port", "--server.address=0.0.0.0"]