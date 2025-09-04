# 🤖 Multi-Model Agentic Chatbot

**⚠️ Disclaimer: This is a developmental prototype, not a final production application.** I am actively learning and building. Future updates will include advanced features like RAG (Retrieval-Augmented Generation), more sophisticated agent frameworks, and a complete frontend rebuild with HTML/CSS/JS.

A powerful and experimental chatbot built with LangGraph, featuring multi-LLM support, persistent memory, and a suite of tools to perform real-world tasks. It demonstrates the core concepts of AI agents with reasoning and tool-use capabilities.

[![Built with LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-blue)](https://langchain-ai.github.io/langgraph/)
[![Streamlit](https://img.shields.io/badge/Interface-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

*   **🤖 Multi-LLM Backend**: Leverages the best models for different tasks (OpenAI GPT-4.1-nano for tool calling, Google Gemini 2.5-flash for general chat).
*   **🧠 Persistent Memory**: All conversations are automatically saved to a SQLite database, allowing users to resume old chats seamlessly.
*   **� Agentic Workflow**: Built on **LangGraph**, enabling complex reasoning, tool selection, and action execution in a cyclic graph pattern.
*   **� Versatile Toolset**: Equipped with 11+ tools to interact with the world:
    *   `tavily_search`, `wikipedia_search`, `arxiv_search` (Information Retrieval)
    *   `get_stock_price`, `convert_currency` (Finance)
    *   `get_weather`, `get_news` (Real-time Data)
    *   `calculator`, `unit_converter` (Calculation & Conversion)
    *   `get_joke`, `get_quote` (Entertainment)
*   **💬 Streamlit UI**: A simple and functional web interface for interacting with the chatbot.
*   **📁 Chat Management**: Start new chats or resume any previous conversation from a sidebar list.

## 🛠️ Built With

*   **Framework**: [LangGraph](https://langchain-ai.github.io/langgraph/) + [LangChain](https://www.langchain.com/)
*   **LLMs**: [Google Gemini 2.5 Flash](https://aistudio.google.com/) / [OpenAI GPT-4.1-nano](https://openai.com/) (via `langchain_google_genai` & `langchain_openai`)
*   **Memory & Checkpointing**: `SqliteSaver` for persistent graph state storage.
*   **Frontend**: [Streamlit](https://streamlit.io/)
*   **Database**: SQLite
*   **Environment Management**: `python-dotenv`

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd your-project-directory
    ```

2.  **Create a virtual environment (recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *If you don't have a `requirements.txt`, install the core packages:*
    ```bash
    pip install langgraph langchain-google-genai langchain-openai streamlit python-dotenv
    ```

4.  **Set up Environment Variables**
    Create a `.streamlit/secrets.toml` file for your API keys (the Streamlit standard):
    ```toml
    # .streamlit/secrets.toml
    GROQ_API_KEY = "your_groq_api_key_here"
    OPENAI_API_KEY = "your_openai_api_key_here"
    GEMINI_API_KEY = "your_gemini_api_key_here" # If needed by the Google LLM
    TAVILY_API_KEY = "your_tavily_api_key_here" # If needed by the tavily_search tool
    ```
    *You must obtain these API keys from their respective providers.*

5.  **Run the Application**
    ```bash
    streamlit run app.py
    ```
    Replace `app.py` with the actual name of your Streamlit application file.

## 🚀 Usage

1.  The Streamlit app will open in your browser.
2.  The sidebar lists all your previous chat sessions. Click on one to resume.
3.  To start a new conversation, click "New Chat" in the sidebar.
4.  Type your message in the input box and press Enter.
5.  Watch the agent reason, call tools if necessary, and provide a response!
6.  Example queries to test the tools:
    *   "What's the weather like in Paris?"
    *   "What's the current stock price for Apple (AAPL)?"
    *   "Search for recent papers by Yann LeCun on arxiv."
    *   "Convert 100 USD to EUR."
    *   "Tell me a joke."

## 🧠 How It Works: The LangGraph Flow

The core of the chatbot is a LangGraph `StateGraph` that manages the conversation flow:

1.  **State**: The `ChatState` holds the list of messages in the conversation.
2.  **Start**: A new user message (`HumanMessage`) enters the graph.
3.  **Chat Node**: The message is passed to the LLM (GPT-4.1-nano), which is bound to the available tools. The LLM decides to either:
    *   **Answer** directly, ending the cycle, or
    *   **Request a tool call**.
4.  **Conditional Edge**: The `tools_condition` function checks the LLM's response. If it contains tool calls, the graph routes to the `Tool Node`.
5.  **Tool Node**: The requested tools (e.g., `get_weather`, `calculator`) are executed, and their results are appended to the message history.
6.  **Loop**: The graph returns to the **Chat Node** with the new tool results. The LLM now synthesizes this information into a final, human-readable response.
7.  **Checkpointing**: After each step, the entire state of the conversation is automatically saved to the `chatbot.db` SQLite database via the `SqliteSaver`.

This loop continues until the LLM provides a final answer without needing more tools.

## 🔮 Future Roadmap / What I'm Learning Next

This project is a foundation for my learning. Here's what I plan to implement next:

*   **RAG (Retrieval-Augmented Generation)**: Integrate a knowledge base from my own documents (PDFs, websites) to provide more specific and grounded answers.
*   **Advanced Agent Patterns**: Implement more complex patterns like hierarchical agents, multi-agent collaboration, and planning.
*   **Production Frontend**: Replace the Streamlit UI with a custom, responsive frontend built with **HTML, CSS, and JavaScript** (likely with a framework like React or Next.js).
*   **Enhanced UX**: Voice input/output, better chat history display, and message editing.
*   **Authentication & Multi-User Support**: Allow different users to have their own isolated chat histories.

## 📁 Project Structure (Overview)
