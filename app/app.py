from fastapi import FastAPI
from query_params.app import router as queryparam_router

app = FastAPI(
    title="Learning FastAPI",
    description="Learning how to build API's using fast api",
    version="1.0.0"
)
app.include_router(queryparam_router)

@app.get("/")
def hello_word():
    return {
        "hello": "World"
    }

@app.get("/health")
def health():
    return {
        "status" : "Healthy",
        "app" : "App is running"
    }