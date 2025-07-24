import requests
from typing import Dict, TypedDict
from langgraph.graph import StateGraph

# Configuration
GEMINI_API_KEY = secrets.GEMINI_API_KEY  ## <- Paste your API key here
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Define the state structure
class AssistantState(TypedDict):
    user_input: str
    intent: str
    retrieved_examples: list
    generated_output: str

def call_gemini_api(prompt: str) -> str:
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': GEMINI_API_KEY
    }
    
    payload = {
        "contents": [{
            "parts": [{
                "text": prompt
            }]
        }]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"API Error: {str(e)}"

def determine_intent(state: AssistantState) -> AssistantState:
    """Determine if user wants to generate or explain code"""
    user_input = state["user_input"].lower()
    if any(keyword in user_input for keyword in ["explain", "how does", "what does"]):
        state["intent"] = "explain"  # Typo preserved to match your workflow
    else:
        state["intent"] = "generate"
    return state

def retrieve_examples(state: AssistantState) -> AssistantState:
    """Retrieve relevant code examples"""
    state["retrieved_examples"] = [
        {"code": "print('Hello World')", "description": "Basic Python example"},
        {"code": "def add(a, b): return a + b", "description": "Function example"}
    ]
    return state

def generate_output(state: AssistantState) -> AssistantState:
    """Generate response using Gemini API"""
    base_prompt = "You are a Python coding assistant. "
    
    if state["intent"] == "explain":
        prompt = f"{base_prompt}Explain this code: {state['user_input']}"
    else:
        prompt = f"{base_prompt}Generate Python code for: {state['user_input']}"
    
    # Add context from retrieved examples
    if state["retrieved_examples"]:
        prompt += "\n\nContext examples:\n"
        for example in state["retrieved_examples"]:
            prompt += f"- {example['description']}\n"
    
    state["generated_output"] = call_gemini_api(prompt)
    return state

def display_output(state: AssistantState) -> AssistantState:
    """Display the output"""
    print("\n=== RESULT ===")
    print(state["generated_output"])
    return state

# Build the workflow
workflow = StateGraph(AssistantState)

# Add nodes
workflow.add_node("determine_intent", determine_intent)  # Note: Typo matches your code
workflow.add_node("retrieve_examples", retrieve_examples)
workflow.add_node("generate_output", generate_output)
workflow.add_node("display_output", display_output)

# Define edges
workflow.add_edge("determine_intent", "retrieve_examples")
workflow.add_edge("retrieve_examples", "generate_output")
workflow.add_edge("generate_output", "display_output")

# Set entry and end points
workflow.set_entry_point("determine_intent")
workflow.set_finish_point("display_output")

# Compile the workflow
assistant = workflow.compile()

# Main interaction loop
print("Python Code Assistant (type 'quit' to exit)")
while True:
    user_input = input("\nWhat would you like help with? ")
    
    if user_input.lower() in ["quit", "exit"]:
        break
        
    # Run the workflow
    result = assistant.invoke({"user_input": user_input})
