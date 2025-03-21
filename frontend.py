import streamlit as st
import uuid
from backend import supervisor, checkpointer
from langchain_core.messages import AIMessage, HumanMessage

# Store the thread ID in session state to persist across interactions
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        AIMessage(content="Hey I am a historical agent AI, You can ask anything around it.")
    ]

# Streamlit UI
st.title("Chat with Monument Agent")

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, AIMessage):
        st.markdown(f"**🤖 Assistant:** {msg.content}")
    elif isinstance(msg, HumanMessage):
        st.markdown(f"**🧑 You:** {msg.content}")

# Function to communicate with the bot
def get_chatbot_response(user_input):
    if not user_input.strip():
        return "Please enter a message."

    # Define the graph
    graph = supervisor.compile(checkpointer=checkpointer)
    thread_config = {"configurable": {"thread_id": st.session_state.thread_id}}

    # Append user input to session state before sending to bot
    user_message = HumanMessage(content=user_input)
    st.session_state.messages.append(user_message)

    # Call the bot
    response = graph.invoke(
        {"messages": st.session_state.messages},
        config=thread_config
    )

    # Debugging: Log response structure
    st.session_state["debug_last_response"] = response

    if not response or "messages" not in response:
        return "Sorry, I couldn't process that."

    # Extract the last AI message
    bot_reply = next(
        (msg.content for msg in reversed(response["messages"]) if isinstance(msg, AIMessage)),
        "Sorry, I couldn't process that."
    )

    return bot_reply

# Input box for user
user_input = st.text_input("Type your message here...", key="user_input")

# Process user input only once per interaction
if st.session_state.get("last_user_input") != user_input and user_input:
    st.session_state.last_user_input = user_input  # Track last input to prevent loops

    bot_response = get_chatbot_response(user_input)
    st.session_state.messages.append(AIMessage(content=bot_response))

    st.rerun()  # Refresh UI to show the latest messages

# Debugging output
if "debug_last_response" in st.session_state:
    with st.expander("Debug Info (last bot response)"):
        st.json(st.session_state["debug_last_response"])
