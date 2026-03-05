import json
import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env into os.environ

# prefer OPENROUTER_API_KEY, fall back to OPENAI_API_KEY for compatibility
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError(
        "API key not found. Set OPENROUTER_API_KEY (or OPENAI_API_KEY) in your environment or .env file."
    )

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

def get_available_flights(origin, destination, date):
    """Fake dataset for the flight"""
    flights = [
        {"flight_number": "AI202", "origin": "New York", "destination": "London", "date": "2023-10-01", "price": 500},
        {"flight_number": "AI203", "origin": "New York", "destination": "Paris", "date": "2023-10-02", "price": 550},
        {"flight_number": "AI204", "origin": "New York", "destination": "Berlin", "date": "2023-10-03", "price": 600},
    ]
    return json.dumps({
        "flights": flights,
        "origins": [flight["origin"] for flight in flights],
        "destinations": [flight["destination"] for flight in flights]
    })


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_available_flights",
            "description": "Get available flights between two cities on a specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {"type": "string", "description": "The departure city (e.g. London)"},
                    "destination": {"type": "string", "description": "The destination city (e.g. Paris)"},
                    "date": {"type": "string", "description": "The date of the flight (YYYY-MM-DD)"}
                },
                "required": ["origin", "destination", "date"]
            }
        }
    }
]

def stream_gpt(message, history):

    messages = [
        {"role": "system", "content": "You are a helpful assistant that can check flights."}
    ]

    # Convert gradio history → OpenAI format
    messages.extend(history or [])

    messages.append({"role": "user", "content": message})

    # FIRST CALL (no streaming to detect tool call)
    response = client.chat.completions.create(
        model="arcee-ai/trinity-large-preview:free",
        messages=messages,
        tools=tools
    )

    msg = response.choices[0].message

    # TOOL CALL
    if msg.tool_calls:

        tool_call = msg.tool_calls[0]
        args = json.loads(tool_call.function.arguments)

        result = get_available_flights(
            args["origin"],
            args["destination"],
            args["date"]
        )

        messages.append(msg)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })

        stream = client.chat.completions.create(
            model="arcee-ai/trinity-large-preview:free",
            messages=messages,
            stream=True
        )

    else:

        stream = client.chat.completions.create(
            model="arcee-ai/trinity-large-preview:free",
            messages=messages,
            stream=True
        )

    full_text = ""

    for chunk in stream:
        if not chunk.choices:
            continue

        delta = chunk.choices[0].delta

        if hasattr(delta, "content") and delta.content:
            full_text += delta.content
            yield full_text
        
chat = gr.ChatInterface(fn=stream_gpt, examples=["hello", "HeHE", "merhaba"], title="Trinity Chat")
chat.launch(inbrowser=True)
