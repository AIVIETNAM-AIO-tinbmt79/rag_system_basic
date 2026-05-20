import streamlit as st
import requests

from rag_system_basic.rag_system.frontend.utils.auth import (
    save_token
)

API_URL = "http://127.0.0.1:8000"


def show_login():

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.title("Login")

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            response = requests.post(
                f"{API_URL}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                token = response.json()[
                    "access_token"
                ]

                save_token(token)

                st.rerun()

            else:

                st.error(
                    "Invalid credentials"
                )

        st.divider()

        if st.button(
            "Create account",
            use_container_width=True
        ):

            st.session_state.screen = (
                "register"
            )

            st.rerun()