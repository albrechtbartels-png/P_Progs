# Dockerfile für Solar Dashboard
# Verwendet ein leichtes Python-Image

FROM python:3.10-slim

# Setze Umgebungsvariablen
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installiere Systemabhängigkeiten (für Tkinter)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tk \
    && rm -rf /var/lib/apt/lists/*

# Setze das Arbeitsverzeichnis
WORKDIR /app

# Kopiere Anforderungen und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den Quellcode
COPY src/ ./src/
COPY run.py .

# Erstelle ein Verzeichnis für Daten
RUN mkdir -p /app/data
VOLUME /app/data

# Setze den Standardbefehl
CMD ["python", "run.py"]

# Alternative: Direkter Start
# CMD ["python", "src/main.py"]
