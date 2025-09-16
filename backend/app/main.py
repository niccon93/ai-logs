from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routers import auth, users, server_accounts, sources, ingest, examples, health

app = FastAPI(title="AI-Logs API")

origins = settings()["CORS_ORIGINS"] or [settings()["FRONTEND_URL"]]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(server_accounts.router)
app.include_router(sources.router)
app.include_router(ingest.router)
app.include_router(examples.router)
