FROM node:20 AS vite-builder

COPY ui /ui
WORKDIR /ui

RUN npm install
RUN npm run build

FROM python:3.13-slim

ENV DB_CONNECTION_STRING="sqlite:///database.db"
ENV PATH="$PATH:/usr/local/bin/docker"

RUN mkdir -p /root/.pip-cache


RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

COPY --from=vite-builder /ui/build /backend/static

COPY backend/requirements.txt /backend/requirements.txt
WORKDIR /backend

RUN pip install --cache-dir=/root/.pip-cache -r requirements.txt

COPY backend /backend

COPY --from=vite-builder /ui/build /app/static

EXPOSE 8080

CMD ["fastapi", "run", "--port", "8080"]