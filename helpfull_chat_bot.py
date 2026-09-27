import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage 
model = ChatGroq(
    model="openai/gpt-oss-120b"
)
message=[
    SystemMessage(content="You are a helpful assistant.")
]
print("Welcome to the Ali Chatbot  Type 'exit' to quit.")
while True:
    prompt=input("you: ")
    message.append(HumanMessage(content=prompt))
    if prompt.lower() == 'exit':
        print("Exiting the chatbot. Goodbye!")
        break
    response = model.invoke(message)
    message.append(AIMessage(content=response.content))
    print("Bot",response.content)

