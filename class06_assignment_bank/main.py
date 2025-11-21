import streamlit as st
import requests

# Set page config for custom styling
st.set_page_config(
    page_title="Royal Bank",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for beige and purple theme
st.markdown("""
<style>
    .stApp {
        background-color: #F5F5DC; /* Beige */
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem 1rem 10rem;
    }
    .stButton>button {
        background-color: #8A2BE2; /* BlueViolet */
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #9370DB; /* MediumPurple */
    }
    h1, h2 {
        color: #4B0082; /* Indigo */
    }
</style>
""", unsafe_allow_html=True)


FASTAPI_URL = "http://127.0.0.1:8000"

st.title("Welcome to the Royal Bank")

# --- Authentication ---
st.header("1. Authenticate")
auth_name = st.text_input("Enter your name:")
auth_pin = st.text_input("Enter your PIN:", type="password")

if st.button("Authenticate"):
    if auth_name and auth_pin:
        try:
            pin = int(auth_pin)
            response = requests.post(
                f"{FASTAPI_URL}/authenticate",
                json={"name": auth_name, "pin_number": pin}
            )
            if response.status_code == 200:
                st.success(f"Authentication successful! Your balance is: ${response.json()['bank_balance']:.2f}")
            else:
                st.error(f"Authentication failed: {response.json().get('detail', 'Unknown error')}")
        except ValueError:
            st.error("PIN must be a number.")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Please ensure it is running.")
    else:
        st.warning("Please enter both name and PIN.")


# --- Bank Transfer ---
st.header("2. Bank Transfer")
sender_name = st.text_input("Your Name (Sender):")
recipient_name = st.text_input("Recipient's Name:")
transfer_amount = st.number_input("Amount to Transfer:", min_value=0.0, format="%.2f")

if st.button("Transfer Funds"):
    if sender_name and recipient_name and transfer_amount > 0:
        try:
            response = requests.post(
                f"{FASTAPI_URL}/bank-transfer",
                json={"sender_name": sender_name, "receipents_name": recipient_name, "amount": transfer_amount}
            )
            if response.status_code == 200:
                res_json = response.json()
                st.success(f"Transfer successful!")
                st.balloons()
            else:
                st.error(f"Transfer failed: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Please ensure it is running.")
    else:
        st.warning("Please fill in all fields for the transfer.")


# --- Deposit ---
st.header("3. Deposit Funds")
deposit_name = st.text_input("Your Name (for Deposit):")
deposit_amount = st.number_input("Amount to Deposit:", min_value=0.0, format="%.2f")

if st.button("Deposit"):
    if deposit_name and deposit_amount > 0:
        try:
            response = requests.post(
                f"{FASTAPI_URL}/deposit",
                json={"name": deposit_name, "amount": deposit_amount}
            )
            if response.status_code == 200:
                st.success(f"Deposit successful! Your new balance is: ${response.json()['updated_balance']:.2f}")
            else:
                st.error(f"Deposit failed: {response.json().get('detail', 'Unknown error')}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the FastAPI server. Please ensure it is running.")
    else:
        st.warning("Please enter your name and a deposit amount.")
