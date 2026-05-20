import streamlit as st


def save_token(token):

    st.session_state["token"] = token


def get_token():

    return st.session_state.get(
        "token"
    )


def is_logged_in():

    return "token" in st.session_state


def logout():

    st.session_state.clear()