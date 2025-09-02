# backend.py

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from helper_tools import arxiv_search, calculator, get_stock_price, wikipedia_search, tavily_search, convert_currency, unit_converter, get_news, get_joke, get_quote, get_weather
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()

groq_api = st.secrets["GROQ_API_KEY"]
openai_api = st.secrets["OPENAI_API_KEY"]

# ------------------
#llm = ChatGroq(model="openai/gpt-oss-120b")
#llm = ChatGroq(model="openai/gpt-oss-20b")
#llm_25_pro = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
#llm_25_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
#llm_25_flash_lite = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
# ✅ 2.0
#llm_20_flash = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
#llm_20_flash_lite = ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")
# ✅ 1.5 (still widely used)
#llm_15_pro = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
#llm_15_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
# ------------------

# -------------------
# 1. LLM
# -------------------
#llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
tool_llm = ChatOpenAI(model="gpt-4.1-nano")
#tool_llm = ChatGroq(model="llama-3.1-8b-instant")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# -------------------
# 2. Tools
# -------------------
# Tools

tools = [get_stock_price, calculator, wikipedia_search, arxiv_search, tavily_search, convert_currency, unit_converter, get_news, get_joke, get_quote, get_weather]
llm_with_tools = tool_llm.bind_tools(tools)

# -------------------
# 3. State
# -------------------
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# -------------------
# 4. Nodes
# -------------------
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call.
    if u do not know anything make sure to use tavily_search,
    do not answer i don't know, this thing is yet to happen until u make sure using the tools"""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

tool_node = ToolNode(tools)

# -------------------
# 5. Checkpointer
# -------------------
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

# -------------------
# 6. Graph
# -------------------
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")

graph.add_conditional_edges("chat_node",tools_condition)
graph.add_edge('tools', 'chat_node')

chatbot = graph.compile(checkpointer=checkpointer)

# -------------------
# 7. Helper
# -------------------
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)



