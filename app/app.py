from fastapi import FastAPI
from app.http.imports.import_controller import import_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to Knitto AI API"}

app.include_router(import_router, prefix="/api", tags=["import"])
