"""
====================================================
OmniRead Backend
====================================================
"""

from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(

    title="OmniRead API",

    description="Backend API for Dyslexia Reading Assistant",

    version="1.0.0"

)

app.include_router(router)