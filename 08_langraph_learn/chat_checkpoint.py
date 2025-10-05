"""
Below code shows how we can take snapshot of the state and store it in the db so that agents have the context of previous conversations
This concept is called checkpointers in langraph and we use mongodb to persist the state data
"""

import os
from dotenv import load_dotenv
from typing import Annotated

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.mongodb import MongoDBSaver

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


with MongoDBSaver.from_conn_string(os.getenv("MONGO_DB_URL")) as checkpointer:
    config = {
        "configurable": {
            "thread_id": "rishikesh"  # this will act as a user_id (case sensitive)
        }
    }
    graph_builder = StateGraph(state_schema=State)

    graph_builder.add_node("chatbot", chatbot)

    # connect nodes using edges
    # (START) -> chatbot -> samplenode -> (END)
    graph_builder.add_edge(START, "chatbot")
    graph_builder.add_edge("chatbot", END)

    # Compile the graph
    graph = graph_builder.compile(checkpointer=checkpointer)

    # updated_state = graph.invoke(
    #     State({"messages": ["Hi, My name is Rishikesh Yadav"]})
    # )
    # print("Updated State : ", updated_state)

    # Stream the response and print the updated state in nice format.
    for chunk in graph.stream(
        State({"messages": ["Hi, what is my name"]}),
        config=config,
        stream_mode="values",
    ):
        # print the last message from the chunk
        chunk["messages"][-1].pretty_print()
