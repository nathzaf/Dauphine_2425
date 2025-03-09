from fastapi import FastAPI

from rest.setup import create_generator_rest_adapter
from rest.endpoint.root import router as root_router

rest_api = FastAPI()

rest_api.include_router(root_router)

generator_rest_adapter = create_generator_rest_adapter()
rest_api.include_router(generator_rest_adapter.get_router())