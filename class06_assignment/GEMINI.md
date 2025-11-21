You are a FastAPI code generator.
Create clean, simple beginner-level FastAPI code exactly as instructed.

Create a file named main.py.

Inside main.py, build a FastAPI instance: 
    app = FastAPI()

Create 3 endpoints:

1. POST /authenticate
   - Inputs: name (string), pin_number (int)
   - Use the users dictionary below to validate:
        users = {
            "ali": {"pin": 1234, "bank_balance": 10000},
            "sara": {"pin": 5678, "bank_balance": 15000}
        }
   - If name or pin incorrect → return error message
   - If correct → return success message + the user’s bank_balance

2. POST /bank-transfer
   - Inputs: sender_name, receipents_name, amount
   - Deduct amount from sender's bank_balance
   - Add amount to receiver's bank_balance
   - Return updated balances for both users

3. POST /deposit
   - Inputs: name, amount
   - Add amount to the user’s bank_balance
   - Return updated_balance

No classes, no database, only dictionary-based storage.
Write complete working FastAPI code only.
