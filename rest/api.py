from fastapi import FastAPI
from rest.endpoint import chat
from rest.setup import create_generator_rest_adapter

app = FastAPI()

generator_rest_adapter = create_generator_rest_adapter()

app.include_router(chat.router, prefix="/chat")