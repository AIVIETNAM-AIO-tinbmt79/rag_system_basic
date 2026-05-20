import json
import streamlit as st
import requests

from rag_system_basic.rag_system.frontend.utils.auth import (
    get_token,
    logout
)

API_URL = "http://127.0.0.1:8000"


def show_chat():

    # =========================
    # SIDEBAR
    # =========================

    with st.sidebar:

        st.title(
            "Business RAG"
        )

        uploaded_file = st.file_uploader(
            "➕ Upload document",
            type=[
                "pdf",
                "docx",
                "txt"
            ]
        )

        if uploaded_file:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file,
                    uploaded_file.type
                )
            }

            headers = {
                "Authorization":
                f"Bearer {get_token()}"
            }

            with st.spinner(
                "Uploading..."
            ):

                response = requests.post(
                    f"{API_URL}/upload/",
                    files=files,
                    headers=headers
                )

            if response.status_code == 200:

                st.success(
                    "Upload success"
                )

            else:

                st.error(
                    response.text
                )

        st.divider()

        if st.button(
            "Logout",
            use_container_width=True
        ):

            logout()

            st.session_state.screen = (
                "login"
            )

            st.rerun()

    # =========================
    # CHAT
    # =========================

    st.title(
        "Business RAG Chat"
    )

    if "messages" not in st.session_state:

        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    query = st.chat_input(
        "Ask something..."
    )

    if query:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": query
            }
        )

        with st.chat_message("user"):
            st.markdown(query)

        headers = {
            "Authorization":
            f"Bearer {get_token()}"
        }

        payload = {
            "query": query,
            "top_k": 5
        }

        with st.chat_message("assistant"):

            answer_placeholder = st.empty()
            full_answer = ""

            try:
                with requests.post(
                    f"{API_URL}/chat/stream",
                    json=payload,
                    headers=headers,
                    stream=True,
                    timeout=(10, 300)  # (connect timeout, read timeout)
                ) as response:

                    if response.status_code == 200:

                        for line in response.iter_lines():
                            if not line:
                                continue

                            # SSE format: "data: {...}"
                            text = line.decode("utf-8")
                            if not text.startswith("data:"):
                                continue

                            data = json.loads(text[5:].strip())

                            if data.get("done"):
                                break

                            if "error" in data:
                                st.error(data["error"])
                                break

                            full_answer += data.get("token", "")
                            answer_placeholder.markdown(full_answer + "▌")

                        answer_placeholder.markdown(full_answer)

                    else:
                        st.error(response.text)

            except Exception as e:
                st.error(f"Connection error: {e}")

        if full_answer:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_answer
                }
            )