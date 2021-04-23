from typing import Optional
from fastapi import FastAPI
from controller import controller

app = FastAPI()


@app.get("/histogram")
def histogram(type):
    return controller.get_histogram(0)
