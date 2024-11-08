**LLaMA AI Assistant**

This project is a chatbot interface powered by the LLaMA language model using the Groq API, built with Streamlit for a simple and interactive user experience.

   **Features**

- Real-time chat interface powered by LLaMA
- User-friendly interface built with Streamlit
- Customizable settings for model parameters like temperature, max tokens, and top-p

   Installation

1.   **Clone the repository**  :
    ```bash
    git clone https://github.com/your-username/llama-ai-assistant.git\n
    cd llama-ai-assistant
    ```

2.   **Install dependencies**  :
    Make sure you have Python 3.10.2 installed. Install dependencies from the `requirements.txt` file:\n
    ```bash
    pip install -r requirements.txt
    ```

   **Configuration**

- The API key and model parameters are stored in `constants.py`. Modify this file to adjust the model settings.

   **Usage**

Run the Streamlit app:

```bash
streamlit run Main.py
