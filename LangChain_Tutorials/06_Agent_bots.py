from typing import TypedDict,List
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START,END
from dotenv import load_dotenv # used to store secret stuff

load_dotenv()

class AgentState(TypedDict):
    messages: List[HumanMessage]

llm = ChatOpenAI(model='gpt-4o') # 1106 is needed for function calling

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")


graph = StateGraph(AgentState)
graph.add_node("process",process)
graph.add_edge(START,'process')
graph.add_edge("process",END)

agent = graph.compile()

user_input = input("Enter:  ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter:   ")
































