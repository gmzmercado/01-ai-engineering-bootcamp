import streamlit as st
from core.config import config
from openai import OpenAI
from groq import Groq
from google import genai


## Let's create a sidebar with a dropdown for the model list and providers
with st.sidebar:
    st.title("Settings")
    
    # Dropdown for the model list
    provider = st.selectbox("Provider", ["OpenAI", "Groq", "Google"])
    
    if provider == "OpenAI":
        model_name = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"])
    elif provider == "Groq":
        model_name = st.selectbox("Model", ["llama-3.3-70b-versatile"])
    elif provider == "Google":
        model_name = st.selectbox("Model", ["gemini-2.0-flash"])
    
    # Save provider and model to session state
    st.session_state.provider = provider
    st.session_state.model_name = model_name

# Ask for API key respective to the user's selection
if st.session_state.provider == "OpenAI":
    client = OpenAI(api_key=config.OPENAI_API_KEY)
elif st.session_state.provider == "Groq":
    client = Groq(api_key=config.GROQ_API_KEY)
elif st.session_state.provider == "Google":
    client = genai.Client(api_key=config.GOOGLE_API_KEY)


# Define a function called run_llm
def run_llm(client, messages, max_tokens=500):
    # Google has a different API for generating content.
    if st.session_state.provider == "Google":
        return client.models.generate_content(
            model=st.session_state.model_name,
            contents=[message["content"] for message in messages]
        ).text

    # All other clients (OpenAI and Groq) use the chat.completions.create API.
    else:
        return client.chat.completions.create(
            model=st.session_state.model_name,
            messages=messages,
            max_tokens=max_tokens
        ).choices[0].message.content

# First steps here.
# client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist  you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Hello, how can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        output = run_llm(client, st.session_state.messages)
        
        # This part does not interest us anymore.
        # output = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": m["role"], "content": m["content"]}
        #         for m in st.session_state.messages
        #     ],
        #     max_tokens=500
        # )
        
    #     st.write(output.choices[0].message.content)
    # st.session_state.messages.append({"role": "assistant", "content": output})

        if output:
            st.write(output)
            st.session_state.messages.append({"role": "assistant", "content": output})