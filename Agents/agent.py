import ollama
import json


# -----------------------------
# TOOL
# -----------------------------

def lookup_order(order_id):
    orders = {
        "123": "Order 123 is shipped.",
        "456": "Order 456 is processing.",
        "789": "Order 789 has been delivered."
    }

    return orders.get(
        order_id,
        f"Order {order_id} was not found."
    )


# -----------------------------
# TOOL DISPATCHER
# -----------------------------

def dispatch(tool_name, arguments):

    if tool_name == "lookup_order":
        return lookup_order(arguments["order_id"])

    return "Unknown tool."


# -----------------------------
# AGENT
# -----------------------------

def run_agent(question, max_steps=4):

    messages = [
        {
            "role": "system",
            "content": """
You are an order support agent.

You have one tool:

lookup_order(order_id)

Use this tool when the user asks about an order.

When you need the tool, return ONLY valid JSON:

{
  "action": "lookup_order",
  "arguments": {
    "order_id": "123"
  }
}

When you already have enough information to answer,
return ONLY valid JSON:

{
  "action": "finish",
  "answer": "your final answer"
}

Do not use any other actions.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(max_steps):

        print(f"\n--- Agent step {step + 1} ---")

        response = ollama.chat(
            model="llama3.2",
            messages=messages,
            options={
                "temperature": 0
            }
        )

        content = response["message"]["content"]

        print("Model:", content)

        try:
            decision = json.loads(content)
        except json.JSONDecodeError:
            return "Agent returned invalid JSON."

        action = decision.get("action")

        # -----------------------------
        # FINISH
        # -----------------------------

        if action == "finish":

            return decision.get(
                "answer",
                "No answer provided."
            )

        # -----------------------------
        # TOOL
        # -----------------------------

        if action == "lookup_order":

            arguments = decision.get(
                "arguments",
                {}
            )

            order_id = arguments.get("order_id")

            if not order_id:
                return "Invalid tool arguments."

            result = dispatch(
                action,
                arguments
            )

            print("Tool result:", result)

            messages.append({
                "role": "assistant",
                "content": content
            })

            messages.append({
                "role": "user",
                "content": f"""
Tool result:

{result}

Now decide whether you need another approved action
or whether you can finish the answer.
"""
            })

            continue

        return f"Denied action: {action}"

    return "Maximum agent steps reached."


# -----------------------------
# CALL THE AGENT
# -----------------------------

question = "What is the status of order 123?"

answer = run_agent(question)

print("\n==============================")
print("FINAL ANSWER:")
print(answer)
print("==============================")
