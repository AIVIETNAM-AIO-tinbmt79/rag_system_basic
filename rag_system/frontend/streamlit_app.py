import streamlit as st

from rag_system_basic.rag_system.frontend.screens.login import show_login
from rag_system_basic.rag_system.frontend.screens.register import show_register
from rag_system_basic.rag_system.frontend.screens.chat import show_chat

from rag_system_basic.rag_system.frontend.utils.auth import (
    is_logged_in
)

st.set_page_config(
    page_title="Business RAG Chat",
    layout="wide"
)

# =========================
# INIT SCREEN
# =========================

if "screen" not in st.session_state:

    st.session_state.screen = "login"

# =========================
# AUTH FLOW
# =========================

if is_logged_in():

    show_chat()

else:

    if st.session_state.screen == "login":

        show_login()

    elif st.session_state.screen == "register":

        show_register()