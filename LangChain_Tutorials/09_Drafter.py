from typing import Annotated,Sequence,TypedDict
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage,HumanMessage,SystemMessage,ToolMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode

load_dotenv()

# This is global variable to store document contents

document_content= ""

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages]

@tool
def update(content: str) -> str:
    """ Updates the document with provided contents"""
    global document_content
    document_content = content 
    return f"Document has been updated successfully!!! The current cotent is :\n{document_content}"

@tool
def save(filename: str) -> str:
    """ Save the current document to a text file and finsih the process.

    Args:
        filename: Name for the tesxt file.
        content: Content to be written to the text file.
    """
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"

    try:
        with open(filename,'w') as file:
            file.write(document_content)
        print(f"\n Document has been saved to : {filename}")
        return f"Document has been saved successfully to '{filename}'. The process has been finished."
    except Exception as e:
        return f"Error Occured while saving document to '{filename}'. Error: {str(e)}"
    
tools = [update,save]

model = ChatOpenAI(model='gpt-4o').bind_tools(tools)

def our_agent(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content=f"""
    You are Drafter, a helpful writing assistant. You are going to help the user update and modify documents.
    
    - If the user wants to update or modify content, use the 'update' tool with the complete updated content.
    - If the user wants to save and finish, you need to use the 'save' tool.
    - Make sure to always show the current document state after modifications.
    
    The current document content is :{document_content}
    """
    )
    if not state['messages']:
        user_input = "I'm ready to help you update a document. What would you like to create ?"
        user_message = HumanMessage(content= user_input)

    else:
        user_input = input("\n What would you like to do next with document ?")
        print(f"\n  USER: {user_input}")
        user_message = HumanMessage(content= user_input)
    all_messages = state["messages"] + list(state['messages'] + [user_message])
    response = model.invoke(all_messages)

    print(f"\n  ASSISTANT: {response.content}")
    if hasattr(response,'tool_calls') and response.tool_calls:
        print(f" USINF TOOL CALL: {[tc["name"] for tc in response.tool_calls]}")
    
    return {"messages": list(state["messages"]) + [user_message,response]}

def should_continue(state: AgentState) -> str:
    """ Determine of we should continue or end the conversation"""

    messages = state["messages"]

    if not messages:
        return "continue"

    # This looks for most recent tool message...abs

    for message in reversed(messages):
        # ... and check if this is ToolMessage resulting from save 
        if (isinstance(message,ToolMessage) and 
            'saved' in message.content.lower() and 
            "document" in message.content.lower()):
            return "end" # Goes to the end edge which leads to endpoints
    return "continue"
    
def print_messages(messages):
    """ Funciton I made to print the message in more redable format """ 
    if not messages:
        return 

    for message in messages[-3:]:
        if isinstance(message,ToolMessage):
            print(f"\n TOOL RESULT: {message.content}")


graph =  StateGraph(AgentState)
graph.add_node("agent",our_agent)
graph.add_node('tools',ToolNode(tools))

graph.set_entry_point("agent")

graph.add_edge("agent","tools")

graph.add_conditional_edges(
    "tools",
    should_continue,
    {
        "continue":"agent",
        "end": END,
    }
)


app = graph.compile()


def run_document_agent():
    print("\n ===== DRAFTER =======")

    state = {"message": []}

    for step in app.stream(state,stream_mode="values"):
        if "messages" in step:
            print_messages(step["messages"])
    
    print("\n ============== DRAFTER FINISHED ==========")

if __name__ == "__main__":
    run_document_agent()