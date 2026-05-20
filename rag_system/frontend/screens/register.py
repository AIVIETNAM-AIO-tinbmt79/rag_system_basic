import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"


def show_register():

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.title("Register")

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button(
            "Register",
            use_container_width=True
        ):

            response = requests.post(
                f"{API_URL}/auth/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password
                }
            )

            if response.status_code == 200:

                st.success(
                    "Register success"
                )

                st.session_state.screen = (
                    "login"
                )

                st.rerun()

            else:

                st.error(
                    response.text
                )

        st.divider()

        if st.button(
            "Back to login",
            use_container_width=True
        ):

            st.session_state.screen = (
                "login"
            )

            st.rerun()