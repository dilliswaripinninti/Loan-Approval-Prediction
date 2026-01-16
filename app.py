import streamlit as st
import numpy as np
import joblib
import os
import random

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Royal Loan Approval",
    page_icon="💰",
    layout="centered"
)

# ---------------- THEME + MONEY RAIN ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: gold;
    overflow-x: hidden;
}
h1, h2, h3 {
    color: gold;
    text-align: center;
    font-family: 'Georgia';
}
.card {
    background: rgba(0,0,0,0.6);
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 0 30px rgba(255,215,0,0.7);
    margin-bottom: 20px;
}

/* BUTTON */
.stButton>button {
    background: linear-gradient(90deg, #d4af37, #ffd700);
    color: black;
    font-size: 18px;
    border-radius: 12px;
    padding: 10px 26px;
    box-shadow: 0 0 20px gold;
}

/* MONEY FALL ANIMATION */
.money {
    position: fixed;
    top: -50px;
    font-size: 30px;
    animation: fall linear infinite;
    z-index: 9999;
}

@keyframes fall {
    to {
        transform: translateY(110vh);
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------- SIDEBAR ----------------
st.sidebar.title("💎 Navigation")
st.sidebar.markdown("Elite Banking System")

choice = st.sidebar.radio(
    "Go to",
    ["Home", "Applicant Profile", "Financial Details", "Loan Result"]
)
st.session_state.page = choice

# ---------------- HOME PAGE ----------------
if st.session_state.page == "Home":
    st.markdown("<h1>💰 Royal Loan Approval System</h1>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
    <h3>Welcome to the Elite Financial Gateway</h3>
    <p>AI-powered loan approval with royal experience.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- APPLICANT PROFILE ----------------
elif st.session_state.page == "Applicant Profile":
    st.markdown("<h1>👤 Applicant Profile</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    name = st.text_input("Full Name")
    age = st.number_input("Age", 18, 70)
    education = st.selectbox("Education", ["Graduate", "Post Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])

    if st.button("Save & Continue 💎"):
        st.session_state.profile = {
            "name": name,
            "age": age,
            "education": education,
            "self_employed": self_employed
        }
        st.success("Profile Saved Successfully!")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FINANCIAL DETAILS ----------------
elif st.session_state.page == "Financial Details":
    st.markdown("<h1>💳 Financial Details</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    income = st.number_input("Applicant Income", 0)
    co_income = st.number_input("Co-Applicant Income", 0)
    loan_amount = st.number_input("Loan Amount (in thousands)", 0)
    credit_history = st.selectbox("Credit History", ["Good (1)", "Bad (0)"])
    credit_history = 1 if credit_history == "Good (1)" else 0

    if st.button("Proceed to Result 👑"):
        st.session_state.finance = {
            "income": income,
            "co_income": co_income,
            "loan_amount": loan_amount,
            "credit_history": credit_history
        }
        st.success("Financial Details Saved!")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- LOAN RESULT ----------------
elif st.session_state.page == "Loan Result":
    st.markdown("<h1>🏆 Loan Approval Result</h1>", unsafe_allow_html=True)

    if "finance" not in st.session_state:
        st.warning("Please complete all previous steps.")
        st.stop()

    # MODEL OR FALLBACK
    try:
        model = joblib.load("loan_amount_model.pkl")
        X = np.array([[ 
            st.session_state.finance["income"],
            st.session_state.finance["co_income"],
            st.session_state.finance["loan_amount"],
            st.session_state.finance["credit_history"]
        ]])
        prediction = model.predict(X)[0]
    except:
        prediction = 1 if st.session_state.finance["credit_history"] == 1 else 0

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    if prediction == 1:
        st.success("🎉 CONGRATULATIONS! LOAN APPROVED")
        st.markdown("💸 *Money is falling from the sky!*")

        # 🎵 SUCCESS SOUND
        if os.path.exists("sounds/money.mp3"):
            st.audio("sounds/money.mp3", autoplay=True)

        # 💸 MONEY FALLING EFFECT
        money_html = ""
        for _ in range(30):
            left = random.randint(0, 100)
            duration = random.uniform(2, 5)
            money_html += f"""
            <div class="money" style="left:{left}%; animation-duration:{duration}s;">
                💰
            </div>
            """
        st.markdown(money_html, unsafe_allow_html=True)

    else:
        st.error("❌ Loan Rejected")
        st.markdown("🔒 Improve credit score and income")

    st.markdown("</div>", unsafe_allow_html=True)
