import nest_asyncio
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from .api.routes import router
from .config.config import API_TITLE, API_VERSION, API_DESCRIPTION, ALLOWED_ORIGINS

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Create FastAPI application
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(
        "alx_connect.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 