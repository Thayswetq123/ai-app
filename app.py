import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

st.title("🧠 KI App")

if "user_id" not in st.session_state:
    st.session_state.user_id = None

menu = st.sidebar.selectbox("Menü", ["Login", "Register", "Dashboard"])

if menu == "Register":
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Registrieren"):
        r = requests.post(f"{API}/register", params={"username": u, "password": p})
        st.write(r.json())

elif menu == "Login":
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        r = requests.post(f"{API}/login", params={"username": u, "password": p})
        res = r.json()

        if "user_id" in res:
            st.session_state.user_id = res["user_id"]
            st.success("Erfolgreich!")
        else:
            st.error("Fehler")

elif menu == "Dashboard":
    if not st.session_state.user_id:
        st.warning("Bitte einloggen")
    else:
        file = st.file_uploader("Bild")

        if file:
            r = requests.post(
                f"{API}/detect/",
                params={"user_id": st.session_state.user_id},
                files={"file": file.getvalue()}
            )

            data = r.json()["detections"]
            df = pd.DataFrame(data)

            st.dataframe(df)
