import os
from aioboto3 import Session
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
SENDER = os.getenv("SES_SENDER_EMAIL")

print(f"SES_SENDER_EMAIL loaded: {SENDER}")


async def send_otp_email(to_email: str, otp: str):
    subject = "Your OTP Code"
    body = f"Your OTP is: {otp}. It is valid for 2 minutes."

    session = Session()
    async with session.client("ses", region_name=AWS_REGION,
                              endpoint_url="https://localhost.localstack.cloud:4566") as client:
        await client.send_email(
            Source=SENDER,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject},
                "Body": {"Text": {"Data": body}}
            }
        )
