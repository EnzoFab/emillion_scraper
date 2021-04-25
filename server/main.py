from typing import Optional
from fastapi import FastAPI
from controller import controller

app = FastAPI()


@app.get("/histogram")
def histogram(histogram_type: str = "numbers"):
    htype = 1 if histogram_type.lower() == "stars" else 1

    return controller.get_histogram(htype)


@app.get("/random_draws")
def random_draw(count: int = 1):
    return controller.get_random_draws(count)
