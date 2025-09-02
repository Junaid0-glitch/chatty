import streamlit as st
from streamlit import session_state
from chatbot_backend import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import uuid
import time

# Page configuration
st.set_page_config(
    page_title="Aurevo",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling to match Claude UI
st.markdown("""
<style>
/* Custom fonts matching Claude */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');

/* Dark theme and general styling */
.stApp {
    background-color: #1a1a1a;
    color: #e0e0e0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 800px;
}

/* Sidebar styling */
.css-1d391kg, .css-1x8cf1d {
    background-color: #2b2b2b;
}

.sidebar .sidebar-content {
    background-color: #2b2b2b;
}

/* Custom sidebar title */
.sidebar-title {
    font-size: 24px;
    font-weight: 600;
    color: #ffffff;
    padding: 20px 0 10px 0;
    margin-bottom: 20px;
}

/* New chat button styling */
.new-chat-btn {
    background-color: #d97706;
    color: white;
    border: none;
    padding: 12px 16px;
    border-radius: 8px;
    font-weight: 500;
    width: 100%;
    margin-bottom: 24px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
}

.new-chat-btn:hover {
    background-color: #b45309;
}

/* Navigation items */
.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
    color: #9ca3af;
    font-size: 14px;
    margin-bottom: 8px;
}

.nav-icon {
    width: 20px;
    height: 20px;
}

/* Recents section */
.recents-section {
    margin-top: 32px;
    margin-bottom: 32px;
}

.recents-title {
    color: #9ca3af;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 12px;
}

.recent-item {
    color: #d1d5db;
    font-size: 14px;
    padding: 6px 0;
    cursor: pointer;
    border-radius: 4px;
    padding-left: 8px;
    margin-bottom: 4px;
}

.recent-item:hover {
    background-color: #374151;
}

/* About button */
.about-btn {
    background-color: #374151;
    color: #d1d5db;
    border: none;
    padding: 12px 16px;
    border-radius: 8px;
    font-weight: 400;
    width: 100%;
    margin-bottom: 16px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14px;
}

.about-btn:hover {
    background-color: #4b5563;
}

/* About section modal/expandable */
.about-section {
    background-color: #374151;
    padding: 16px;
    border-radius: 8px;
    font-size: 12px;
    color: #d1d5db;
    line-height: 1.4;
    margin-bottom: 16px;
    border: 1px solid #4b5563;
}

/* Welcome message */
.welcome-container {
    text-align: center;
    padding: 60px 0 40px 0;
}

.welcome-greeting {
    font-family: 'Crimson Text', Georgia, serif;
    font-size: 32px;
    font-weight: 400;
    color: #ffffff;
    margin-bottom: 8px;
}

.welcome-emoji {
    font-size: 40px;
    margin-bottom: 16px;
}

.welcome-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 16px;
    color: #9ca3af;
    margin-bottom: 40px;
}

/* Custom input styling */
.input-container {
    position: relative;
    max-width: 600px;
    margin: 0 auto;
}

/* Message styling */
.message-user {
    background-color: #374151;
    color: #ffffff;
    padding: 16px 20px;
    border-radius: 16px;
    margin: 8px 0;
    margin-left: auto;
    margin-right: 0;
    max-width: 80%;
    float: right;
    clear: both;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.5;
}

.message-assistant {
    background-color: #1f2937;
    color: #e5e7eb;
    padding: 16px 20px;
    border-radius: 16px;
    margin: 8px 0;
    margin-left: 0;
    margin-right: auto;
    max-width: 80%;
    float: left;
    clear: both;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
    line-height: 1.6;
    font-weight: 400;
}

.tool-notice {
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    color: #9ca3af;
    margin-top: 8px;
    font-style: italic;
    font-weight: 400;
}

/* Tool animation */
.tool-animation {
    display: inline-flex;
    align-items: center;
    gap: 8px;
}

.tool-spinner {
    width: 16px;
    height: 16px;
    border: 2px solid #374151;
    border-top: 2px solid #d97706;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.tool-pulse {
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

/* Hide streamlit components */
.stDeployButton {display:none;}
footer {visibility: hidden;}
.stApp > header {visibility: hidden;}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
}

::-webkit-scrollbar-thumb {
    background: #4b5563;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #6b7280;
}
</style>
""", unsafe_allow_html=True)

# =========================== Utilities ===========================
def generate_thread_id():
    return uuid.uuid4()

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []
    st.session_state["chat_started"] = False
    st.session_state["show_about"] = False  # Hide about when starting new chat
    st.rerun()

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={"configurable": {"thread_id": thread_id}})
    return state.values.get("messages", [])

def get_thread_preview(thread_id):
    """Get a preview of the first message in a thread"""
    try:
        messages = load_conversation(thread_id)
        if messages:
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                    return preview
        return f"Chat {str(thread_id)[:8]}..."
    except:
        return f"Chat {str(thread_id)[:8]}..."

# ======================= Session Initialization ===================
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads()

if "show_welcome" not in st.session_state:
    st.session_state["show_welcome"] = True

if "chat_started" not in st.session_state:
    st.session_state["chat_started"] = False

if "show_about" not in st.session_state:
    st.session_state["show_about"] = False

add_thread(st.session_state["thread_id"])

# ============================ Sidebar ============================
with st.sidebar:
    # App title
    st.markdown('<div class="sidebar-title">Aurevo</div>', unsafe_allow_html=True)
    
    # New chat button
    if st.button("🔄 New chat", key="new_chat_btn"):
        reset_chat()
    
    # About button
    if st.button("ℹ️ About", key="about_btn"):
        st.session_state["show_about"] = not st.session_state["show_about"]
    
    # Show about section if toggled
    if st.session_state["show_about"]:
        st.markdown("""
        <div class="about-section">
            Hey, it's Juddy! I created this app using LangGraph. First, I built a simple frontend to confirm the direction I wanted to take. Then, I used AI to generate an attractive and responsive frontend with HTML and CSS since I'm not very experienced in frontend development. However, I designed and built the entire backend and implemented all the logic myself.Feel free to share your feedback or suggestions—I’d love to hear from you!
        </div>
        """, unsafe_allow_html=True)
    
    # Recents section - Show actual chat threads
    if st.session_state["chat_threads"]:
        st.markdown('<div class="recents-title">Recents</div>', unsafe_allow_html=True)
        
        # Show recent threads (reversed to show newest first)
        for thread_id in reversed(st.session_state["chat_threads"][-10:]):  # Show last 10 threads
            if thread_id != st.session_state["thread_id"]:  # Don't show current thread
                thread_preview = get_thread_preview(thread_id)
                if st.button(thread_preview, key=f"thread_{thread_id}"):
                    st.session_state["thread_id"] = thread_id
                    messages = load_conversation(thread_id)
                    
                    temp_messages = []
                    for msg in messages:
                        if isinstance(msg, HumanMessage):
                            temp_messages.append({"role": "user", "content": msg.content})
                        elif isinstance(msg, AIMessage):
                            temp_messages.append({"role": "assistant", "content": msg.content, "used_tools": False})
                    
                    st.session_state["message_history"] = temp_messages
                    st.session_state["chat_started"] = len(temp_messages) > 0
                    st.rerun()

# ============================ Main UI ============================

# Always show welcome message at the top
st.markdown("""
<div class="welcome-container">
    <div class="welcome-emoji">🌟</div>
    <div class="welcome-greeting">What can I help you with today?</div>
</div>
""", unsafe_allow_html=True)

# Render message history if there are messages
if st.session_state["message_history"]:
    for message in st.session_state["message_history"]:
        if message["role"] == "user":
            st.markdown(f'<div class="message-user">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-assistant">{message["content"]}</div>', unsafe_allow_html=True)
            # Check if this message was generated with tools
            if message.get("used_tools", False):
                tool_names = message.get("tool_names", [])
                if tool_names:
                    if len(tool_names) == 1:
                        tool_text = f"This answer was generated with the help of {tool_names[0]}."
                    else:
                        tool_text = f"This answer was generated with the help of {', '.join(tool_names[:-1])} and {tool_names[-1]}."
                else:
                    tool_text = "This answer was generated with the help of external tools."
                st.markdown(f'<div class="tool-notice">{tool_text}</div>', unsafe_allow_html=True)

# Input area
user_input = st.chat_input("How can I help you today?")

if user_input:
    # Mark that chat has started
    st.session_state["chat_started"] = True
    
    # Add user message to history
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    
    # Display user message
    st.markdown(f'<div class="message-user">{user_input}</div>', unsafe_allow_html=True)
    
    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_turn",
    }
    
    # Create a placeholder for the assistant's response
    response_placeholder = st.empty()
    
    # Track if tools were used and create status holder
    status_holder = {"box": None, "tools_used": False, "tool_names": []}
    
    def ai_stream_with_ui():
        response_text = ""
        
        for message_chunk, metadata in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages",
        ):
            # Handle tool usage
            if isinstance(message_chunk, ToolMessage):
                status_holder["tools_used"] = True
                tool_name = getattr(message_chunk, "name", "tool")
                if tool_name not in status_holder["tool_names"]:
                    status_holder["tool_names"].append(tool_name)
                
                if status_holder["box"] is None:
                    status_holder["box"] = st.status(
                        f"🔧 Using `{tool_name}` …", expanded=True
                    )
                    # Add animation
                    with status_holder["box"]:
                        st.markdown("""
                        <div class="tool-animation">
                            <div class="tool-spinner"></div>
                            <span class="tool-pulse">Processing with {tool_name}...</span>
                        </div>
                        """.format(tool_name=tool_name), unsafe_allow_html=True)
                else:
                    status_holder["box"].update(
                        label=f"🔧 Using `{tool_name}` …",
                        state="running",
                        expanded=True,
                    )
            
            # Stream assistant messages
            if isinstance(message_chunk, AIMessage):
                response_text += message_chunk.content
                # Update the response in real-time
                response_placeholder.markdown(
                    f'<div class="message-assistant">{response_text}</div>', 
                    unsafe_allow_html=True
                )
        
        return response_text
    
    # Get the assistant's response
    assistant_response = ai_stream_with_ui()
    
    # Finalize tool status if tools were used
    if status_holder["box"] is not None:
        status_holder["box"].update(
            label="✅ Tool finished", state="complete", expanded=False
        )
    
    # Add assistant message to history
    st.session_state["message_history"].append({
        "role": "assistant", 
        "content": assistant_response,
        "used_tools": status_holder["tools_used"],
        "tool_names": status_holder["tool_names"]
    })
    
    # Auto-scroll to bottom (Streamlit limitation - this is a workaround)
    time.sleep(0.1)
    st.rerun()

# Add some spacing at the bottom
st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)