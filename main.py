from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scripts.core.routes import all_routers


from scripts.config import ModuleConfig

app = FastAPI(
    title="User Management API",
    description="API for managing users, roles, and permissions",
    version="1.0.0",
    contact={
        "name": "Hemanth Kumar Pasham",
        "email": "hemanthkumarpasham9502@gmail.com",
    },
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "Users",
            "description": "Operations related to user management",
        },
        {
            "name": "Roles",
            "description": "Operations related to role management",
        },
        {
            "name": "Permissions",
            "description": "Operations related to permission management",
        },
    ]
)

app.include_router(all_routers, prefix="/user_mngmt")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ModuleConfig.CORS_ORIGINS,  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns a simple message indicating the API is healthy.
    """
    return {"status": "healthy", "message": "User Management API is running!"}

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that provides a welcome message.
    Returns a simple message indicating the API is running.
    """
    return {"message": "Welcome to the User Management API!"}

