from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Fake database
users = {
    "ali": {"pin": 1234, "bank_balance": 10000},
    "sara": {"pin": 5678, "bank_balance": 15000},
    "samiya": {"pin": 7890, "bank_balance": 30000},
    "umaiza": {"pin": 8031,"bank_balance": 700000}
    }

# Data Models
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

# Homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Authenticate
@app.post("/authenticate")
async def authenticate_user(details: AuthDetails):
    name = details.name.lower()
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if users[name]["pin"] != details.pin_number:
        raise HTTPException(status_code=401, detail="Invalid PIN")
    return {"message": "Authentication successful", "user": name}

# Bank Transfer
@app.post("/bank-transfer")
async def bank_transfer(details: TransferDetails):
    sender = details.sender_name.lower()
    receiver = details.receipents_name.lower()
    amount = details.amount
    if sender not in users or receiver not in users:
        raise HTTPException(status_code=404, detail="Sender or recipient not found")
    if users[sender]["bank_balance"] < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    users[sender]["bank_balance"] -= amount
    users[receiver]["bank_balance"] += amount
    return {
        "message": "Transfer successful",
        "sender_balance": users[sender]["bank_balance"],
        "receiver_balance": users[receiver]["bank_balance"]
    }

# Deposit Money
@app.post("/deposit")
async def deposit(details: DepositDetails):
    name = details.name.lower()
    amount = details.amount
    if name not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[name]["bank_balance"] += amount
    return {
        "message": "Deposit successful",
        "updated_balance": users[name]["bank_balance"]
    }
