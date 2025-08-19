import streamlit as st
from passlib.hash import sha256_crypt

# Session state to track login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Simulated database (replace with real DB)
users_db = {}

def register(username, password):
    if username in users_db:
        st.error("❌ Username already exists!")
    else:
        hashed_password = sha256_crypt.hash(password)
        users_db[username] = hashed_password
        st.success("✅ Registration successful! Please log in.")

def login(username, password):
    if username not in users_db:
        st.error("❌ Username not found!")
    elif not sha256_crypt.verify(password, users_db[username]):
        st.error("❌ Incorrect password!")
    else:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.success("✅ Login successful!")

# UI
if st.session_state.logged_in:
    st.title(f"Welcome, {st.session_state.username}!")
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
else:
    st.title("Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            login(username, password)

    with tab2:
        new_username = st.text_input("New Username")
        new_password = st.text_input("New Password", type="password")
        if st.button("Register"):
            register(new_username, new_password)
