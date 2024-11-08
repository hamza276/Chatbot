# llama_chatbot.py
import streamlit as st
import constants
from groq import Groq

# Streamlit app configuration
st.set_page_config(
    page_title="LLaMA AI Assistant",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize the Groq client with the API key
groq_client = Groq(api_key=constants.GROQ_API_KEY)

# Initialize session state to store chat history and input clearing flag
if "messages" not in st.session_state:
    st.session_state.messages = []
if "clear_input" not in st.session_state:
    st.session_state.clear_input = False
if "is_waiting" not in st.session_state:
    st.session_state.is_waiting = False

def send_message():
    user_input = st.session_state.user_input.strip()
    if user_input and not st.session_state.is_waiting:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.is_waiting = True

        try:
            completion = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]} for msg in st.session_state.messages],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
                stop=None
            )
            if completion and hasattr(completion, 'choices') and len(completion.choices) > 0:
                response_text = completion.choices[0].message.content
                if response_text:
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": "No response from LLaMA API."})
            else:
                st.session_state.messages.append({"role": "assistant", "content": "No response from LLaMA API."})
        
        except Exception as e:
            error_message = f"Error calling LLaMA API: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.error(error_message)

        st.session_state.clear_input = True
        st.session_state.is_waiting = False

# Display chat title and description with enhanced styling
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #2E4057; font-size: 2.5em; margin-bottom: 10px;'>LLaMA AI Assistant</h1>
        <p style='color: #666; font-size: 1.2em;'>Your intelligent companion powered by LLaMA technology</p>
    </div>
""", unsafe_allow_html=True)

# Create a container for the chat messages
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f"""<div style='display: flex; justify-content: flex-end; margin-bottom: 12px;'>
                    <div style='background-color: #E3F2FD; padding: 12px 16px; border-radius: 15px 15px 0 15px; 
                    max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); color: #1565C0;'>
                        {message['content']}
                    </div>
                </div>""", 
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""<div style='display: flex; justify-content: flex-start; margin-bottom: 12px;'>
                    <div style='background-color: #F5F5F5; padding: 12px 16px; border-radius: 15px 15px 15px 0; 
                    max-width: 80%; box-shadow: 0 1px 2px rgba(0,0,0,0.1); color: #333;'>
                        {message['content']}
                    </div>
                </div>""", 
                unsafe_allow_html=True
            )

# Input area with enhanced styling
if st.session_state.clear_input:
    st.session_state.user_input = ""
    st.session_state.clear_input = False

st.markdown("""
    <style>
    /* Main container styling */
    .stApp {
        background-color: #FFFFFF;
    }

    /* Chat container styling */
    .stMarkdown {
        max-width: 800px;
        margin: 0 auto;
    }

    /* Input field styling */
    .stTextInput > div > div > input {
        Position:fixed
        background-color: #F8F9FA;
        border: 2px solid #E9ECEF;
        border-radius: 12px;
        padding: 12px 20px;
        font-size: 16px;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #2E4057;
        box-shadow: 0 0 0 2px rgba(46,64,87,0.1);
    }

    /* Placeholder text styling */
    .stTextInput > div > div > input::placeholder {
        color: #ADB5BD;
    }

    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #F1F3F4;
    }

    ::-webkit-scrollbar-thumb {
        background: #CED4DA;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #ADB5BD;
    }

    /* Error message styling */
    .stAlert {
        border-radius: 8px;
        margin-top: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

# Input field with enhanced placeholder
user_input = st.text_input(
    "",
    key="user_input",
    placeholder="Type your message here... Press Enter to send",
    on_change=send_message
)