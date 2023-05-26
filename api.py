import os
import json
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_summary(code_to_summarize: str):
    prompt = "Please list each method in the following code along with input parameters and return parameters and the minimum description required to understand its functionality. We do not care about UI, only functionality. Please follow this example format in your response:\nMethod: get_all_filepaths(folder: string)\nReturns: A list of all filepaths in the inputted folder\nDescription: this method recursively iterates through a list of all files in the given folder and returns them as a list\n\n" + code_to_summarize
    gpt35_turbo_message = [
        {
            "role": "system",
            "content": "You are a world-class software architect and developer."
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=gpt35_turbo_message,
            max_tokens=300,
            temperature=0,
        )

        # extract the response content
        print(response)
        response_content = response['choices'][0]['message']['content'].strip()

        return response_content

    except Exception as error:
        raise error
