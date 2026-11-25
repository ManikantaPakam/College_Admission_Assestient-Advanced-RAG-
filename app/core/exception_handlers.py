import logging
from fastapi.exceptions import RequestValidationError
from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


async def global_exception_handler(
    request: Request,
    exc: Exception
):
    logger.error(
        "Unhandled exception occurred | Path: %s | Error: %s",
        request.url.path,
        str(exc),
        exc_info=(type(exc), exc, exc.__traceback__)
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "Something went wrong. Please try again later."
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    logger.warning(
        "Request validation failed | Path: %s",
        request.url.path
    )

    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(str(item) for item in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": errors
        }
    )