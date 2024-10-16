import openai
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os


_ = load_dotenv(find_dotenv())
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def chat_with_gpt(messages):
    chat_gpt_response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages,
        temperature = 0,
        max_tokens = 500
    )

    token_dict = {
        'prompt_tokens': chat_gpt_response.usage.prompt_tokens,
        'completion_tokens': chat_gpt_response.usage.completion_tokens,
        'total_tokens': chat_gpt_response.usage.total_tokens,
    }
    # print(chat_gpt_response)
    return chat_gpt_response.choices[0].message.content.strip(), token_dict

# code to be executed when the script run directly
if __name__ == '__main__':
    chat_context = []
    while True:
        user_input = input('You: ')
        if user_input.lower() in ['quit', 'q', 'bye', 'exit']:
            break

        chat_context.append({'role' : 'user', 'content': user_input})

        moderator = client.moderations.create(
            model="omni-moderation-latest",
            input=user_input)
        response_dict = moderator.model_dump()
        prompt_flagged = response_dict['results'][0]['flagged']

        if prompt_flagged:
            print("\nI am sorry but your message was flagged by moderator. Try again.\n")
        else:
            response, tokens = chat_with_gpt(chat_context)
            print("Chatbot: ", response)
            print("----------------------\nTokens used in this session: ")
            for type_of_usage in tokens:
                print(type_of_usage, ": ", tokens[type_of_usage])

            chat_context.append({'role': 'assistant', 'content': str(response)})


# make the context of all the responses