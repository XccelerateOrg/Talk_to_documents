import streamlit as st
import os
import shutil
from config import upload_dir
from doc_processor import process_file, process_query
from AI_model import get_answer


def sidebar():
    my_sidebar = st.sidebar
    my_sidebar.title("File upload")
    with my_sidebar.form(key='file-handler'):
        uploaded_files = st.file_uploader(label="Text Files",
                                          type="txt",
                                          accept_multiple_files=True,
                                          key='pdf_upload')
        submitted = st.form_submit_button("Upload")

        if submitted:
            with st.spinner("Wait for the process to finish..."):
                if os.path.exists(upload_dir):
                    shutil.rmtree(upload_dir)
                os.makedirs(upload_dir)
                for fl in uploaded_files:
                    with open(os.sep.join([upload_dir, fl.name]), "wb") as f:
                        f.write(fl.getbuffer())
                for f in uploaded_files:
                    process_file(os.sep.join([upload_dir, f.name]))
            st.write("Upload successful!")


def main():
    sidebar()
    st.title("Chat bot")
    # handle chats till now
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["message"])

    if query := st.chat_input("Ask a question!"):
        with st.chat_message("user"):
            st.markdown(query)
            st.session_state.messages.append({"role": "user",
                                              "message": query})
        with st.chat_message("assistant"):
            # bot_response = f"Echo: {query}"
            context = process_query(query)
            bot_response = get_answer(query, context['documents'][0][0])
            st.markdown(bot_response)
            st.session_state.messages.append({"role": "assistant",
                                              "message": bot_response})


if __name__ == '__main__':
    main()
