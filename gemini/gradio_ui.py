import os

import gradio as gr
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-pro')

def handle_user_query(msg, chatbot):
    print(msg, chatbot)
    chatbot += [[msg, None]]
    return '', chatbot
def generate_chatbot(chatbot: list[list[str, str]]) -> list[list[str, str]]:
    formatted_chatbot = []
    if len(chatbot) == 0:
        return formatted_chatbot
    for ch in chatbot:
        formatted_chatbot.append(
            {
                "role": "user",
                "parts": [ch[0]]
            }
        )
        formatted_chatbot.append(
            {
                "role": "model",
                "parts": [ch[1]]
            }
        )
    return formatted_chatbot

def handle_gemini_response(chatbot):
    query = chatbot[-1][0]
    formated_chatbot = generate_chatbot(chatbot[:-1])
    chat = model.start_chat(history=formated_chatbot)
    response = chat.send_message(query)
    chatbot[-1][1] = response.text
    # chatbot[-1][1] = "From the function."
    return chatbot

with gr.Blocks() as demo:
    chatbot = gr.Chatbot(
        label = "Chat with Gemini",
        bubble_full_width=False,
    )
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(
        handle_user_query,
        [msg, chatbot],
        [msg, chatbot]
    ).then(
        handle_gemini_response,
        [chatbot],
        [chatbot]
    )

if __name__== "__main__":
    demo.queue()
    demo.launch()