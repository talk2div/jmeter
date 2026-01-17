from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import uvicorn
import uuid

app = FastAPI(title="Mock Enterprise API")

# -----------------------
# Models
# -----------------------

class LoginRequest(BaseModel):
    username: str
    otp: str

class SubmitRequest(BaseModel):
    application_id: str
    amount: float

# -----------------------
# Helpers
# -----------------------

def validate_token(token: str):
    if not token or not token.startswith("mock-token-"):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

# -----------------------
# APIs
# -----------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mock Enterprise API. Please refer to the documentation for available endpoints."}

@app.post("/login")
def login(data: LoginRequest):
    # Mock OTP check
    if data.otp != "123456":
        raise HTTPException(status_code=401, detail="Invalid OTP")

    token = f"mock-token-{uuid.uuid4()}"
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/profile")
def get_profile(authorization: str = Header(None)):
    token = authorization.replace("Bearer ", "") if authorization else None
    validate_token(token)

    # Simulate backend latency
    # time.sleep(0.2) # Removed for immediate response

    return {
        "user": "demo-user",
        "role": "citizen",
        "status": "active"
    }

@app.post("/submit-application")
def submit_application(
    data: SubmitRequest,
    authorization: str = Header(None)
):
    token = authorization.replace("Bearer ", "") if authorization else None
    validate_token(token)

    # Simulate heavy processing (Process API)
    # time.sleep(1.5) # Removed for immediate response

    return {
        "application_id": data.application_id,
        "status": "SUBMITTED",
        "processing_time_sec": 1.5
    }

@app.get("/health")
def health():
    return {"status": "UP"}

if __name__ == "__main__":
    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
