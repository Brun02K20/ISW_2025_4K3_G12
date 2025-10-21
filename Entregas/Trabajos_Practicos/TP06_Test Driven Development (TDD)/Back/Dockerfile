FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN ls -la
RUN chmod +x start_services.sh
EXPOSE 8080
CMD ["/app/start_services.sh"]
