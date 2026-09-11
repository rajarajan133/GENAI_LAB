Understand what happened

This line:

chain = hello | welcome

is the important part.

It means:

"Rajarajan"
      ↓
    hello
      ↓
"Hello Rajarajan"
      ↓
   welcome
      ↓
"Hello Rajarajan - Welcome to LangChain!"

And:

chain.invoke("Rajarajan")

starts the pipeline.

This is LCEL

LCEL = LangChain Expression Language

The | operator lets you compose runnable components.
