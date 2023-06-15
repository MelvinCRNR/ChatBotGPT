import os

import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message

from utils import get_initial_message, get_chatgpt_response, update_chat

load_dotenv()
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

st.title("Mon assistant en ligne")
st.subheader("Créé par Melvin CRENIER:")

model = st.selectbox(
    "Choisissez une version de ChatGpt",
    ("gpt-3.5-turbo", "gpt-4")
)

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Requête: ", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        # st.write("Before  making the API call")
        # st.write(messages)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated']) - 1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        message(st.session_state["generated"][i], key=str(i))

    with st.expander("Show Messages"):
        st.write(messages)
