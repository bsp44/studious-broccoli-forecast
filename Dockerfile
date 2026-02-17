FROM python:3.12-slim

WORKDIR /app

COPY requirements-forecast.txt .
RUN pip install --no-cache-dir -r requirements-forecast.txt

COPY marketing_forecast.py .
COPY templates/ templates/

ENV PORT=10000
EXPOSE 10000

# Render injects PORT at runtime; Gunicorn binds to 0.0.0.0:$PORT
CMD gunicorn --bind 0.0.0.0:${PORT} marketing_forecast:app
