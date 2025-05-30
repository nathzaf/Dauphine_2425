from fastapi import FastAPI
from infrastructure.config.dependency_injection import container
from rest.endpoint.root import router as root_router

rest_api = FastAPI()

rest_api.include_router(root_router)

# Chat endpoints
rest_api.include_router(container.chat_controller.get_router())

# Document endpoints
rest_api.include_router(container.document_controller.get_router())