from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os


_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(messages):
    chat_gpt_response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages,
        temperature = 0
    )

    return chat_gpt_response.choices[0].message.content.strip()

# code to be executed when the script run directly
if __name__ == '__main__':
    chat_context = []
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['quit', 'q', 'bye', 'exit']:
            break

        chat_context.append({'role' : 'user', 'content': user_input})

        response = chat_with_gpt(chat_context)
        print("Chatbot: ", response)

        chat_context.append({'role': 'assistant', 'content': str(response)})

# make the context of all the responses