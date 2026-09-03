from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import test_database_connection
from app.routers.companies import router as companies_router

app = FastAPI(
    title="Estoque Bruna Essence API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies_router)


@app.get("/")
def home():
    return {
        "message": "API Estoque Bruna Essence funcionando!"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/health/database")
def database_health():
    test_database_connection()

    return {
        "status": "ok",
        "database": "postgresql",
    }