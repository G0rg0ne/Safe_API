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

## Deployment on Hetzner Server

### Quick Deploy

To deploy on your Hetzner server:

```bash
# Make the script executable (if needed)
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

This script will:
- Generate SSL certificates (self-signed) if they don't exist
- Build the Docker container
- Start the application with Docker Compose
- Check if the service is running properly

### Making Requests from Your Local Machine

Once deployed, you can make requests from your local machine:

```bash
# Get your Hetzner server IP
# Then use curl with -k flag to accept the self-signed certificate
curl -k https://YOUR_SERVER_IP:443/ping
curl -k https://YOUR_SERVER_IP:443/health
```

### Alternative: Using Let's Encrypt Certificates

For production use with a domain, consider using Let's Encrypt:

```bash
# Install certbot
sudo apt-get update
sudo apt-get install -y certbot

# Generate certificates for your domain
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to the certs folder
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem certs/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem certs/key.pem
sudo chmod 644 certs/cert.pem
sudo chmod 600 certs/key.pem
```

## Port Considerations

**Note:** Port 443 typically requires administrative privileges on most systems. If you encounter permission issues, you can:

1. Run with sudo (Linux/Mac): `sudo docker-compose up --build`
2. Or modify the port mapping in `docker-compose.yml` to use a higher port number like `8000:443`
