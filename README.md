# (any LLM) Chat — Gradio UI for OpenRouter GPT

Lightweight Gradio chat UI that streams responses from an OpenRouter/OpenAI-compatible LLM. The app uses the OpenAI Python client configured to talk to OpenRouter (base_url = https://openrouter.ai/api/v1) and serves a streaming chat interface via Gradio.

## Features

- Simple streaming chat UI using Gradio
- Uses OpenRouter-compatible models (configured via API key)
- Minimal codebase — easy to adapt to other models or inputs

## Typical use cases

- Rapidly demoing an LLM conversational model to non-technical stakeholders
- Experimenting with streaming responses and UI/UX for chat assistants
- Prototyping AI assistants for customer support, brainstorming, or tutoring
- Research and testing for different model prompts, system messages, and streaming strategies

## Prerequisites

- Linux machine (tested)
- Python 3.8+
- An OpenRouter API key

## Installation

1. Create and activate a virtual environment:
   sudo apt install python3-venv # if venv not installed
   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:
   pip install gradio openai python-dotenv

3. Add your API key to a `.env` file in the project root:
   OPENROUTER_API_KEY=your_openrouter_api_key_here

## Running

From the project root:
python gradioUI.py

The script launches a Gradio interface (it opens the default browser when `inbrowser=True`). Use the UI to send messages; responses stream back as they are produced.

## Notes & troubleshooting

- Environment variable name: the code expects `OPENROUTER_API_KEY`.
- If Gradio raises errors about undefined inputs (e.g., `message_input` or `model_selector`), the chat interface expects defined Gradio components. You can replace `input=[message_input, model_selector]` with a single textbox, for example:
  - Example quick fix (in `gradioUI.py`): replace the ChatInterface `input=` argument with `input=gr.Textbox(placeholder="Type a message...")`.
- If you see authentication or connection errors, verify the key and network access to `https://openrouter.ai`.
- Streaming behavior depends on the model and the OpenRouter endpoint supporting streaming.

## Security

- Do not commit your `.env` or API keys. Add `.env` to `.gitignore` if not already ignored.

## License

MIT
