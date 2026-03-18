from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error caught: {exc}", exc_info=True)

    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred in the system."}
    )