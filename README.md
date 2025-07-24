# 🧠 Python Code Assistant with LangGraph + Gemini API

This project implements a **smart Python code assistant** using [LangGraph](https://docs.langgraph.dev) for state management and the **Gemini 2.0 Flash** model by Google for natural language understanding and code generation.

It allows users to:
- 💡 Explain Python code  
- ⚙️ Generate Python code  
- 📚 Get relevant examples  
- 🧩 Interact via a modular state machine

---

## 📌 Features

- ✨ Natural language intent detection (generate vs. explain)  
- 🤖 Gemini 2.0 Flash model integration via HTTP API  
- 🔁 Example retrieval for better context  
- 🔧 Modular graph-based architecture with LangGraph  

---

## 📂 Project Structure

```
📦 LangGraph Code Assistant
┣ assistant.py                   # Main code assistant script
┣ LICENSE                        # permissive license
┣ week4-langgraph.ipynb          # Code Notebook
┣ README.md                      # Project documentation
```

---

## 🧠 How It Works

This assistant is built using a **LangGraph `StateGraph`** with the following states:

1. **`determine_intent`** – Understand if the user wants to *generate* or *explain* code.  
2. **`retrieve_examples`** – Provide basic examples to assist the model.  
3. **`generate_output`** – Craft a prompt and call Gemini API for a response.  
4. **`display_output`** – Print the result to the console.  

---

## 📬 Example Interaction

```text
> What would you like help with?
Explain: def greet(name): return "Hello " + name

=== RESULT ===
This function takes a name as input and returns a greeting string by concatenating "Hello " with the provided name.
```

---

## 🧑‍💻 Author

**Mohamed Montasser**  
---

## 📝 License

MIT License – use, modify, share freely!
