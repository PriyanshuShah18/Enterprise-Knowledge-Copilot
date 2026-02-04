import streamlit as st
import requests
import os

# ---------------- CONFIG ----------------
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"  # local fallback
)
st.write("API_BASE_URL =", API_BASE_URL)

st.set_page_config(
    page_title="Enterprise Knowledge Copilot",
    page_icon="📄",
    layout="wide",
)

# ---------------- SESSION STATE ----------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "documents_uploaded" not in st.session_state:
    st.session_state.documents_uploaded = False

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Controls")

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 📂 Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload one or more documents",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
    )

    if uploaded_file:
        with st.spinner("Uploading & indexing documents..."):
            files_payload = [
                ("files", (file.name, file.getvalue(), file.type))
                for file in uploaded_file
            ]

            try:
                response = requests.post(
                    f"{API_BASE_URL}/upload",
                    files=files_payload,
                    timeout=300,
                )
            except requests.exceptions.RequestException:
                st.error("❌ Backend is unreachable. Please try again later.")
                st.stop()

            if response.status_code == 200:
                st.success("✅ Documents uploaded successfully")
                st.session_state.documents_uploaded = True
            else:
                st.error("❌ Upload failed")

# ---------------- HEADER ----------------
st.title("📄 Enterprise Knowledge Copilot")
st.caption("Ask questions from uploaded documents • RAG-based")
st.divider()

# ---------------- CHAT DISPLAY ----------------
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.write(message)

# ---------------- CHAT INPUT ----------------
user_query = st.chat_input("Ask a question from the uploaded documents")

if user_query:
    if not st.session_state.documents_uploaded:
        st.warning("⚠️ Please upload at least one document first.")
    else:
        # User message
        st.session_state.chat_history.append(("user", user_query))
        with st.chat_message("user"):
            st.write(user_query)

        # Backend call
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/chat",
                        params={"query": user_query},
                        timeout=120,
                    )
                except requests.exceptions.RequestException:
                    st.error("❌ Backend is unreachable. Please try again later.")
                    st.stop()

                if response.status_code == 200:
                    answer = response.json().get("answer", "")
                else:
                    answer = "❌ Error from backend"

                st.write(answer)

        st.session_state.chat_history.append(("assistant", answer))

# ---------------- FOOTER ----------------
st.divider()
st.markdown(
    "<center><small>🔒 Privacy-first • FastAPI + Gemini • RAG Architecture</small></center>",
    unsafe_allow_html=True,
)
