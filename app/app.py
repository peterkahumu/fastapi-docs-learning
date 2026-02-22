from fastapi import FastAPI
from query_params.app import router as queryparam_router
from request_body.app import router as body_router
from query_params_and_string_validations.app import router as qpstringvalidation
from body_multiple_params.app import body_multiple_params as body_multiple_params
from body_fields.app import body_field
from nested_models.app import app as nested_models_router
from extra_data_types.app import router as extra_data_types_router
app = FastAPI(
    title="Learning FastAPI",
    description="Learning how to build API's using fast api",
    version="1.0.0"
)

app.include_router(queryparam_router)
app.include_router(body_router)
app.include_router(qpstringvalidation)
app.include_router(body_multiple_params)
app.include_router(body_field)
app.include_router(nested_models_router)
app.include_router(extra_data_types_router)

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