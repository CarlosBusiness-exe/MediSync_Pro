from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router
from core.exceptions import global_exception_handler

app: FastAPI = FastAPI(title="MediSync - Medical System")
app.include_router(api_router, prefix=settings.API_V1_STR)
app.add_exception_handler(Exception, global_exception_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)