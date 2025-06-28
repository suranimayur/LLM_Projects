from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage # The foundational class of all message types in LangGrah
from langchain_core.messages import ToolMessage
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode


load_dotenv()

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

@tool
def add (a:int, b:int):
    """ This is an addition function that adds 2 numbers togather"""
    return a + b 

@tool
def substract (a:int, b:int):
    """ This is an substraction function that substracts 2 numbers togather"""
    return a - b 


@tool
def multiply (a:int, b:int):
    """ This is an multiplication function that multiplies 2 numbers togather"""
    return a * b 


tools = [add,substract,multiply]

model = ChatOpenAI(model='gpt-4o').bind_tools(tools)

def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are my AI Assistance. Please answer my queries to best of your ability")
    response = model.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [response]}

def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "end"
    else:
        return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent",model_call)

tool_node = ToolNode(tools=tools)
graph.add_node("tools",tool_node)


graph.set_entry_point("our_agent")
graph.add_conditional_edges(
    "our_agent",
    should_continue,
    {
        "continue": "tools",
        "end": END,
    },
)

graph.add_edge("tools","our_agent")

app = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message,tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user","Add 40 and 90 and then multiply it with 129 and substract 1000 and tell joke")]}
print_stream(app.stream(inputs,stream_mode='values'))














