import streamlit as st

# ---------------------------
# Fake database
# ---------------------------
users = {
    "ali": {"pin": 1234, "bank_balance": 10000},
    "sara": {"pin": 5678, "bank_balance": 15000},
    "samiya": {"pin": 7890, "bank_balance": 30000},
    "umaiza": {"pin": 8031, "bank_balance": 700000},
    
}

# ---------------------------
# Initialize session state
# ---------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "message" not in st.session_state:
    st.session_state.message = ""
if "last_recipient" not in st.session_state:
    st.session_state.last_recipient = None

# ---------------------------
# Custom CSS for buttons
# ---------------------------
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #6a0dad;
        color: white;
        height: 40px;
        width: 100%;
        border-radius:10px;
        font-size:16px;
        font-weight:bold;
    }
    div.stButton > button:first-child:hover {
        background-color: #560a9d;
        color:white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Title
# ---------------------------
st.title("💳 Mini Bank App")
st.write("Authenticate first, then transfer money. See recipient's balance below transfer box.")

# ---------------------------
# Authenticate User
# ---------------------------
with st.form("auth_form"):
    st.markdown("### 🔐 Authenticate")
    username = st.text_input("Name", key="auth_name")
    pin = st.text_input("PIN Number", type="password", key="auth_pin")
    submitted = st.form_submit_button("Authenticate")

    if submitted:
        uname = username.lower()
        if uname not in users:
            st.session_state.message = "❌ User not found."
            st.session_state.authenticated = False
            st.session_state.current_user = None
        elif not pin.isdigit() or int(pin) != users[uname]["pin"]:
            st.session_state.message = "❌ Invalid PIN."
            st.session_state.authenticated = False
            st.session_state.current_user = None
        else:
            st.session_state.authenticated = True
            st.session_state.current_user = uname
            st.session_state.message = f"✅ Authentication successful! Welcome {uname}."

if st.session_state.message:
    st.info(st.session_state.message)

# ---------------------------
# Only show Transfer after authentication
# ---------------------------
if st.session_state.authenticated:
    current_user = st.session_state.current_user

    # Display current balance dynamically
    st.subheader(f"💰 {current_user}'s Current Balance: ${users[current_user]['bank_balance']:.2f}")

    # ---------------------------
    # Transfer Money
    # ---------------------------
    with st.form("transfer_form"):
        st.markdown("### 💸 Bank Transfer")
        st.text_input("Sender", value=current_user, disabled=True)
        recipient = st.text_input("Recipient Name", key="transfer_recipient")
        amount = st.number_input("Amount", min_value=0.01, step=0.01, key="transfer_amount")
        transfer_sub = st.form_submit_button("Send Money")

        if transfer_sub:
            rec = recipient.lower()
            if rec not in users:
                st.error("❌ Recipient not found.")
            elif users[current_user]["bank_balance"] < amount:
                st.error("❌ Insufficient balance.")
            else:
                users[current_user]["bank_balance"] -= amount
                users[rec]["bank_balance"] += amount
                st.success(f"✅ Transfer successful! New balance for {current_user}: ${users[current_user]['bank_balance']:.2f}")
                st.session_state.last_recipient = rec  # store last recipient

    # Display current balance after transfer
    st.subheader(f"💰 {current_user}'s Current Balance: ${users[current_user]['bank_balance']:.2f}")

    # Display recipient's balance if a transfer just happened
    if st.session_state.last_recipient:
        recipient_name = st.session_state.last_recipient
        st.subheader(f"💰 {recipient_name.capitalize()}'s Updated Balance: ${users[recipient_name]['bank_balance']:.2f}")
