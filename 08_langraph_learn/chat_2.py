"""
This example shows how to create conditional edge using langGraph
"""

from dotenv import load_dotenv
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from openai import OpenAI

load_dotenv()

client = OpenAI()


class State(TypedDict):
    user_query: str
    llm_output: str
    is_goog: bool


# Node
def chatbot(state: State):
    response = client.responses.create(
        model="gpt-4.1-mini", input=state.get("user_query")
    )

    state["llm_output"] = response.output_text
    return state


# Conditional Edge
def evaluate_response(state: State) -> Literal["chatbot_gpt_5", "end_node"]:
    # for now assuming the response is not good
    if False:
        # return the id of the node
        return "end_node"

    return "chatbot_gpt_5"


# Node
def chatbot_gpt_5(state: State):
    response = client.responses.create(model="gpt-5", input=state.get("user_query"))

    state["llm_output"] = response.output_text
    return state


# End Node
def end_node(state: State):
    return state


graph_builder = StateGraph(state_schema=State)

# add nodes in the graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("chatbot_gpt_5", chatbot_gpt_5)
graph_builder.add_node("end_node", end_node)


# add edges in the graph
graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges(
    "chatbot", evaluate_response
)  # this is a conditional edge
graph_builder.add_edge("chatbot_gpt_5", "end_node")
graph_builder.add_edge("end_node", END)

# compile the graph
graph = graph_builder.compile()

# invoke the graph
updated_state = graph.invoke(input=State({"user_query": "Hey, what is 4 + 4"}))

print("Updated State : ", updated_state)
