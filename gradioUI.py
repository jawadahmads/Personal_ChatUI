import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # This loads variables from .env into os.environ

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
def stream_gpt(message, history):
    # Gradio 6 uses a list of content blocks in 'history'. 
    # OpenAI also supports this format.
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(history)
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="arcee-ai/trinity-large-preview:free",
        messages=messages,
        stream=True,
    )
    result = ""
    for chunk in response:
        #  checking if the streamed output is not None
        if chunk.choices and chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content
            yield result
            

chat = gr.ChatInterface(    
    fn=stream_gpt,
    examples=["hello", "hola", "merhaba"],
    title="Trinity Chat",
    fill_height=True,
    fill_width=True,
)

chat.launch(inbrowser=True)

