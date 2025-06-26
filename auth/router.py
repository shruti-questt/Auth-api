from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from auth.otp_store import store_otp, verify_otp, mark_otp_used
from auth.email import send_otp_email
from auth.jwt_utils import create_jwt_token

router = APIRouter()

class RequestOTP(BaseModel):
    email: EmailStr

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

@router.post("/request-otp")
async def request_otp(data: RequestOTP):
    otp = await store_otp(data.email)
    await send_otp_email(data.email, otp)
    print(f"your otp is {otp}")
    return {"message": "OTP sent successfully"}

@router.post("/verify-otp")
async def verify_otp_route(data: VerifyOTP):
    valid = await verify_otp(data.email, data.otp)
    if not valid:
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")

    await mark_otp_used(data.email, data.otp)
    token = create_jwt_token({"email": data.email})
    return {"access_token": token, "token_type": "bearer"}
