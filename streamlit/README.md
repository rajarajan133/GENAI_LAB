# GENAI_LAB

A small lab for experimenting with LLM-backed apps.

## Files

- `streamlit.py` — Streamlit chat UI ("Prompt Lab"). Uses the OpenAI SDK pointed at
  [OpenRouter](https://openrouter.ai) (`https://openrouter.ai/api/v1`) with the
  `openrouter/free` model. Keeps chat history in `st.session_state` and shows response
  time + token usage under each reply.
- `1_prompt_app.py` — minimal CLI example that calls the OpenAI API directly
  (`gpt-4o-mini`) to answer a single hardcoded question.
- `hello.py` — sanity-check script.

## Setup

```bash
pip install streamlit openai python-dotenv
```

### Environment variables

- `streamlit.py` requires `OPENROUTER_API_KEY` (get one at https://openrouter.ai/keys).
- `1_prompt_app.py` requires `OPENAI_API_KEY`, either exported or in a local `.env` file
  (loaded via `python-dotenv`).

Export permanently in `~/.bashrc`:

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
export OPENAI_API_KEY="sk-..."
```

Then reload the shell (`source ~/.bashrc`) or open a new terminal — env vars set in
`.bashrc` only apply to shells started *after* the change, and a Streamlit process
already running won't pick up an updated key until it's restarted.

## Run

```bash
streamlit run streamlit.py
```

Open the printed local URL (default http://localhost:8501) and start chatting.

```bash
python 1_prompt_app.py
```
