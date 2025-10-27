import uvicorn
from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import os


app = FastAPI(title="Safe API", version="1.0.0")

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"]
)

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Production settings
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=443,
        ssl_keyfile=os.getenv("SSL_KEYFILE", "/app/certs/key.pem"),
        ssl_certfile=os.getenv("SSL_CERTFILE", "/app/certs/cert.pem"),
        workers=4,  # Multiple workers for production
        log_level="info",
        access_log=True
    )