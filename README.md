# FastAPI Ping Pong API

A simple FastAPI application with a ping/pong endpoint, containerized with Docker.

## Setup

### Build and Run with Docker Compose

```bash
docker-compose up --build
```

The API will be available at `http://localhost:443` (or `https://localhost:443` if you have SSL configured).

### Build and Run with Docker

```bash
docker build -t fastapi-app .
docker run -p 443:443 fastapi-app
```

## API Endpoints

### Root Endpoint

**GET** `http://localhost:443/`

```bash
curl http://localhost:443/
```

**Response:**
```json
{
  "message": "FastAPI is running!"
}
```

### Ping Endpoint

**GET** `http://localhost:443/ping`

```bash
curl http://localhost:443/ping
```

**Response:**
```json
{
  "message": "pong"
}
```

## Alternative Endpoints

### Health Check

Visit `http://localhost:443/docs` for the interactive API documentation (Swagger UI).

Visit `http://localhost:443/redoc` for the alternative API documentation (ReDoc).

## Example Usage

### Check if API is running

```bash
curl http://localhost:443/
```

### Ping the API

```bash
curl http://localhost:443/ping
```

### Get verbose output

```bash
curl -v http://localhost:443/ping
```

### Save response to file

```bash
curl -o response.json http://localhost:443/ping
```

## Stopping the Service

If running with Docker Compose:

```bash
docker-compose down
```

If running with Docker:

```bash
docker ps  # Find the container ID
docker stop <container_id>
```

## Requirements

- Docker
- Docker Compose (optional, for docker-compose commands)

## Port Considerations

**Note:** Port 443 typically requires administrative privileges on most systems. If you encounter permission issues, you can:

1. Run with sudo (Linux/Mac): `sudo docker-compose up --build`
2. Or modify the port mapping in `docker-compose.yml` to use a higher port number like `8000:443`
