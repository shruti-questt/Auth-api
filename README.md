.env contents:
REDIS_URL=redis://localhost:6379
JWT_SECRET=your_super_secret_key
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=15
OTP_EXPIRY_SECONDS=500
AWS_ACCESS_KEY_ID=fake
AWS_SECRET_ACCESS_KEY=fake
AWS_REGION=us-east-1
SES_SENDER_EMAIL=test@example.com

# OTP Authentication API

# Authentication API with OTP via Email (FastAPI + Redis + LocalStack SES)

This is a simple FastAPI-based authentication service that uses OTP (One-Time Password) verification via email. OTPs are stored and verified using Redis. Email sending is simulated using Amazon SES via [LocalStack](https://github.com/localstack/localstack).

---

## Features

- Request OTP to an email address
- Verify OTP and return a JWT token
- Redis-based OTP storage with expiry
- Amazon SES email delivery (mocked using LocalStack)
- Prevents OTP reuse by tracking used OTPs in Redis

---

## Tech Stack

- Python 3.12
- FastAPI
- Redis (async)
- aioboto3 + LocalStack (for mocking SES)
- Uvicorn
- pyjwt (JWT tokens)

---

## Prerequisites

- Python 3.12 (use `pyenv` to manage multiple versions)
- Redis installed and running locally (default: `localhost:6379`)
- Docker installed (LocalStack requires Docker)
- LocalStack CLI installed (`pip install localstack`)

---

## Getting Started

### 1. Clone & Setup

```bash
git clone "https://github.com/...."
cd authentication_api
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


4. Run redis server locally
redis-server

5. Start LocalStack using Docker:
localstack start

6. Verify SES email identity in LocalStack
Verify your sender email (replace with your actual sender email):

awslocal ses verify-email-identity --email-address your_email@example.com

7. Create a .env file in the project root with the following variables:
REDIS_URL=redis://localhost:6379
SES_SENDER_EMAIL=your_email@example.com
AWS_REGION=us-east-1
OTP_EXPIRY_SECONDS=120
JWT_SECRET=your_jwt_secret_key


8. Start FastAPI server:
uvicorn main:app --reload

API doc at http://127.0.0.1:8000/docs

API Endpoints
Request OTP
Endpoint: POST /auth/request-otp

Payload: JSON { "email": "user@example.com" }

Description: Sends an OTP to the specified email (via mocked SES) and stores it in Redis.

Example curl: curl -X POST http://127.0.0.1:8000/auth/request-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com"}'


Verify OTP
Endpoint: POST /auth/verify-otp

Payload: JSON { "email": "user@example.com", "otp": "123456" }

Description: Verifies the OTP. On success, returns a JWT access token.

Example curl: curl -X POST http://127.0.0.1:8000/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com", "otp":"123456"}'

Redis Key Usage
OTPs are stored in Redis under the key format:
otp:{email} with a TTL of OTP_EXPIRY_SECONDS (default: 120 seconds)

After successful OTP verification, the OTP is deleted and a new key is stored:
used_otp:{email}:{otp} with value "used" and a TTL of 1 hour

This prevents OTP reuse and allows traceability/debugging of previously used OTPs


Notes
1.LocalStack SES does not send real emails. It only mocks AWS SES API responses.
2.Make sure your sender email is verified in LocalStack SES to avoid MessageRejected errors.
3.Redis must be running locally to store OTPs.
4.JWT tokens are signed with the secret defined in .env.
5.Adjust environment variables as needed.