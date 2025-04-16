from fastapi import FastAPI
import os

app = FastAPI()

@app.post("/predict")
async def predict(input: float):
    return {
        "model": "square",
        "result": input ** 2,
        "pod": os.getenv('POD_NAME', 'unknown')
    }