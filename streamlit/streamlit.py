import os
import time
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Prompt Lab",
    layout="wide"
)

# OpenRouter client
client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):

    # Add user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    st.chat_message("user").markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        t0 = time.perf_counter()

        try:
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=st.session_state.messages,
            )

            answer = response.choices[0].message.content

            st.markdown(answer)

            # Show timing
            elapsed = time.perf_counter() - t0

            if response.usage:
                st.caption(
                    f"{elapsed:.2f}s · "
                    f"{response.usage.total_tokens} tokens"
                )
            else:
                st.caption(f"{elapsed:.2f}s")

            # Save assistant response
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:
            st.error(f"Error: {e}")
