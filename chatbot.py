import streamlit as st
from transformers import pipeline, Conversation
import time

about_us = st.sidebar.subheader("About Us")
detail = st.sidebar.text("""Simplifies AI
Our Vision is to help you succeed in your AI career""")
device = "cpu"
audio_out = st.sidebar.selectbox("Get audio output?", ("yes", "no"))
chat_llm = pipeline(task="conversational", model="facebook/blenderbot-400M-distill", device=device)

if audio_out == "yes":
    audio_llm = pipeline(task="text-to-speech", model="facebook/mms-tts-eng", device=device)

system_prompt = "You are a helpful AI"
chat_history = Conversation([{"role": "system", "content": system_prompt}])

# creating chat session
if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.text_input("Type your prompt here....")  # Fixed typo here

if prompt != "":
    with st.chat_message("user"):
        st.markdown(prompt)
        user_chat = {"role": "user", "content": prompt}
        chat_history.add_message(user_chat)
        st.session_state.messages.append(user_chat)

    try:
        response = chat_llm(chat_history, max_length=1024)  # Fixed typo here
    except Exception as e:  # Catch specific exception to get more information
        error_message = "An error occurred: {}".format(str(e))
        with st.chat_message("assistant"):
            st.markdown(error_message)
        st.stop()  # Stop the execution gracefully

    with st.chat_message('assistant'):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = response.messages[-1]["content"]
        if audio_out == "yes":
            audio_response = audio_llm(assistant_response)
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.1)
            message_placeholder.markdown(full_response + "| ")
        message_placeholder.markdown(full_response)
        if audio_out == "yes":
            st.audio(audio_response["audio"], sample_rate=audio_response["sampling_rate"])
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
