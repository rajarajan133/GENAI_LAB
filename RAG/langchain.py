from langchain_core.runnables import RunnableLambda

# Component 1
def get_name(name):
    return f"Hello {name}"

# Component 2
def make_message(message):
    return message + " - Welcome to LangChain!"

hello = RunnableLambda(get_name)
welcome = RunnableLambda(make_message)

# Connect components
chain = hello | welcome

# Run the chain
result = chain.invoke("Rajarajan")

print(result)
