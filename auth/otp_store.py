import os
import redis.asyncio as redis
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

load_dotenv()
r = redis.from_url(os.getenv("REDIS_URL"))

OTP_EXPIRY = int(os.getenv("OTP_EXPIRY_SECONDS", 120))

def generate_otp():
    return f"{random.randint(100000, 999999)}"

async def store_otp(email: str) -> str:
    otp = generate_otp()
    await r.setex(f"otp:{email}", OTP_EXPIRY, otp)
    return otp

async def verify_otp(email: str, otp: str) -> bool:
    stored_otp = await r.get(f"otp:{email}")
    print(f"OTP IS {otp} for EMAIL {email}")
    if stored_otp and stored_otp.decode() == otp:
        return True
    return False

async def mark_otp_used(email: str, otp: str):
    # Move to used set or list for cleanup if needed
    await r.delete(f"otp:{email}")
    await r.setex(f"used_otp:{email}:{otp}", 3600, "used")

# import asyncio

# async def test_redis():
#     email = "test@example.com"
#     otp = await store_otp(email)
#     print("Stored OTP:", otp)

#     is_valid = await verify_otp(email, otp)
#     print("OTP valid:", is_valid)

#     await mark_otp_used(email, otp)
#     is_valid_after_use = await verify_otp(email, otp)
#     print("OTP valid after marking used:", is_valid_after_use)

# # asyncio.run(test_redis())

# if __name__ == "__main__":
#     asyncio.run(test_redis())

