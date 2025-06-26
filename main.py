from fastapi import FastAPI
from auth.router import router as auth_router

app = FastAPI(title="OTP Auth API")
app.include_router(auth_router, prefix="/auth")
