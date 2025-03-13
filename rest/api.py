from fastapi import FastAPI

from rest.endpoint.chat import router as chat_router
from rest.endpoint.root import router as root_router

rest_api = FastAPI()

rest_api.include_router(root_router)
rest_api.include_router(chat_router)