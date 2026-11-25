import logging

import chromadb
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import (
    CHROMA_DB_DIR,
    COLLECTION_NAME,
    GOOGLE_API_KEY,
    EMBEDDING_MODEL,
)

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health Check"])


@router.get("/health")
def health_check():
    """
    Basic application health check.
    """

    return {
        "status": "healthy",
        "application": "College Admission RAG API"
    }


@router.get("/health/details")
def detailed_health_check():
    """
    Check application configuration and ChromaDB connectivity.
    """

    health_details = {
        "application": "healthy",
        "chromadb": "unknown",
        "configuration": {
            "google_api_key": bool(GOOGLE_API_KEY),
            "embedding_model": bool(EMBEDDING_MODEL),
            "chroma_db_directory": str(CHROMA_DB_DIR),
            "collection_name": COLLECTION_NAME
        }
    }

    try:
        # Connect to the existing persistent ChromaDB
        client = chromadb.PersistentClient(
            path=str(CHROMA_DB_DIR)
        )

        # Verify that the configured collection is accessible
        collection = client.get_collection(
            name=COLLECTION_NAME
        )

        document_count = collection.count()

        health_details["chromadb"] = {
            "status": "healthy",
            "document_count": document_count
        }

    except Exception as exc:
        logger.exception("ChromaDB health check failed")

        health_details["chromadb"] = {
            "status": "unhealthy",
            "error": "ChromaDB is unavailable or collection is missing"
        }

        health_details["status"] = "degraded"

        return JSONResponse(
            status_code=503,
            content=health_details
        )

    health_details["status"] = "healthy"

    return health_details