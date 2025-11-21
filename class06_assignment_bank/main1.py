from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

users = {
    "ali": {"pin": 1234, "bank_balance": 10000},
    "sara": {"pin": 5678, "bank_balance": 15000}
}

class AuthDetails(BaseModel):
    name: str
    pin_number: int

class TransferDetails(BaseModel):
    sender_name: str
    receipents_name: str
    amount: float

class DepositDetails(BaseModel):
    name: str
    amount: float

@app.post("/authenticate")
def authenticate(details: AuthDetails):
    user = users.get(details.name)
    if user and user["pin"] == details.pin_number:
        return {"message": "Authentication successful", "bank_balance": user["bank_balance"]}
    else:
        raise HTTPException(status_code=401, detail="Invalid name or pin")

@app.post("/bank-transfer")
def bank_transfer(details: TransferDetails):
    sender = users.get(details.sender_name)
    recipient = users.get(details.receipents_name)

    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")

    if sender["bank_balance"] < details.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    sender["bank_balance"] -= details.amount
    recipient["bank_balance"] += details.amount

    return {
        "message": "Transfer successful",
        "sender_updated_balance": sender["bank_balance"],
        "recipient_updated_balance": recipient["bank_balance"]
    }

@app.post("/deposit")
def deposit(details: DepositDetails):
    user = users.get(details.name)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user["bank_balance"] += details.amount
    return {"message": "Deposit successful", "updated_balance": user["bank_balance"]}
