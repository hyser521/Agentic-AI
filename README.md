# Agentic AI- A Boot.dev Project
This project is a POC for using Agentic AI, in this case Gemini from Google, commands in conjunction with custom prompt to allow an AI to view/edit/and explore files within a particular working directory.

The AI is primarily used to write, read, and diagnose changes necessary for the calculator app within the project (calculator.py). For example, if someone changes the order of operations for the calculator, it's possible to prompt the AI with "Fix the calculator, **equation** should be **x** not **y**".

Security barriers were also put in place for the AI. It is not allowed to leave the working directory and expects all questions to be related to it and the information within it.
