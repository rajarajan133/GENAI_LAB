from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# 1. Define the shared state
class ResearchState(TypedDict):
    question: str
    route: str
    result: str


# 2. First node: classify the question
def classify(state: ResearchState):
    route = (
        "research"
        if "compare" in state["question"].lower()
        else "knowledge"
    )

    return {"route": route}


# 3. Knowledge node
def answer_from_kb(state: ResearchState):
    return {
        "result": f"Knowledge answer for: {state['question']}"
    }


# 4. Research node
def research(state: ResearchState):
    return {
        "result": f"Research plan for: {state['question']}"
    }


# 5. Decide which node should run next
def choose_route(
    state: ResearchState
) -> Literal["answer_from_kb", "research"]:

    if state["route"] == "research":
        return "research"

    return "answer_from_kb"


# 6. Create the graph
builder = StateGraph(ResearchState)


# 7. Add nodes
builder.add_node("classify", classify)
builder.add_node("answer_from_kb", answer_from_kb)
builder.add_node("research", research)


# 8. Connect START → classify
builder.add_edge(START, "classify")


# 9. Conditional routing
builder.add_conditional_edges(
    "classify",
    choose_route
)


# 10. Connect final nodes → END
builder.add_edge("answer_from_kb", END)
builder.add_edge("research", END)


# 11. Compile the graph
graph = builder.compile()


# 12. Run the graph
result = graph.invoke({
    "question": "Compare two vector stores"
})


# 13. Print result
print("\n==============================")
print("FINAL RESULT")
print("==============================")
print(result)
