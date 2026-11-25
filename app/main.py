import logging
from fastapi import FastAPI
from app.core.logging_config import setup_logging
from app.api.routes.chat import router as chat_router
from fastapi.exceptions import RequestValidationError
from app.api.routes.health import router as health_router
from app.core.rate_limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.v1.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware

from app.core.exception_handlers import (
    global_exception_handler,
    validation_exception_handler
)

from app.core.config import (
    API_DOCS_ENABLED,
    DEBUG
)


setup_logging()

logger = logging.getLogger(__name__)

# Create FastAPI Application
app = FastAPI(
    title="College Admission RAG API",
    description="Advanced RAG Application using Gemini, Hybrid Search and Reranking",
    version="1.0.0",

    debug=DEBUG,

    docs_url="/docs" if API_DOCS_ENABLED else None,

    redoc_url="/redoc" if API_DOCS_ENABLED else None,

    openapi_url="/openapi.json" if API_DOCS_ENABLED else None
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_exception_handler(
    Exception,
    global_exception_handler
)

# Request Validation Exception Handler
app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler
)

# Register Chat Router
app.include_router(chat_router)

# Register Health Router
app.include_router(health_router)

app.include_router(auth_router, prefix="/api/v1")


@app.on_event("startup")
def startup_event():
    logger.info("College Admission RAG API started successfully")


# Root Endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to College Admission RAG API",
        "status": "running"
    }