from langgraph.checkpoint.memory import InMemorySaver

# Create memory/checkpointer
checkpointer = InMemorySaver()

# Compile graph with checkpointing
graph = builder.compile(
    checkpointer=checkpointer
)

# Identify this workflow
config = {
    "configurable": {
        "thread_id": "research-001"
    }
}

# Run workflow
first = graph.invoke(
    {"question": "Compare two vector stores"},
    config=config,
)

# Get latest saved state
latest_state = graph.get_state(config)

print("\n==============================")
print("RESULT")
print("==============================")
print(first["result"])

print("\n==============================")
print("SAVED STATE")
print("==============================")
print(latest_state.values)
