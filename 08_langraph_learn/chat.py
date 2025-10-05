from dotenv import load_dotenv
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

load_dotenv()

llm = init_chat_model(model="gpt-4o-mini", model_provider="openai")


# This is the state of the graph
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]


# Creating this node(function to call by agent)
def chatbot(state: State):
    # invoke the llm
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


def sample_node(state: State):
    return {"messages": ["Sample Message Appended"]}


graph_builder = StateGraph(state_schema=State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sample_node", sample_node)

# connect nodes using edges
# (START) -> chatbot -> samplenode -> (END)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "sample_node")
graph_builder.add_edge("sample_node", END)


# Compile the graph
graph = graph_builder.compile()

updated_state = graph.invoke(State({"messages": ["Hi, My name is Rishikesh Yadav"]}))
print("Updated State : ", updated_state)
