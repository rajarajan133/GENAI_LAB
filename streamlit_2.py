import time, streamlit as st
from openai import OpenAI

st.set_page_config(page_title="Prompt lab", layout="wide")
client = OpenAI()

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).markdown(m["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

    with st.chat_message("assistant"):
        t0 = time.perf_counter()
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=st.session_state.messages,
        )
        answer = r.choices[0].message.content
        st.markdown(answer)
        st.caption(f"{time.perf_counter()-t0:.2f}s · {r.usage.total_tokens} tokens")
        st.session_state.messages.append({"role": "assistant", "content": answer})
