from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import test_database_connection
from app.routers.companies import router as companies_router
from app.routers.users import router as users_router
from app.routers.auth import router as auth_router
from app.routers.categories import router as categories_router
from app.routers.products import router as products_router

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
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)

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