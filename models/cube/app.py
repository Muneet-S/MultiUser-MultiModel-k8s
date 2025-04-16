from fastapi import FastAPI
import os

app = FastAPI()

@app.post("/predict")
async def predict(input: float):
    return {
        "model": "cube",
        "result": input ** 3,
        "pod": os.getenv('POD_NAME', 'unknown')
    }