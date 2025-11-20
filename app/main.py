from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import auth, org, contact, deal, task, activity, analytics

app = FastAPI(title="CRM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(org.router, prefix="/api/v1", tags=["organizations"])
app.include_router(contact.router, prefix="/api/v1", tags=["contacts"])
app.include_router(deal.router, prefix="/api/v1", tags=["deals"])
app.include_router(task.router, prefix="/api/v1", tags=["tasks"])
app.include_router(activity.router, prefix="/api/v1", tags=["activities"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/")
def root():
    return {"message": "CRM API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}