import os
import openai
from dotenv import load_dotenv

class OpenAI_Interface():
    def __init__(self):
        load_dotenv()
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.MODEL="gpt-4"
        self.prompt_tokens=0
        self.completion_tokens=0

    def get_tokens_total(self):
        return self.prompt_tokens, self.completion_tokens

    def get_token_cost(self):
        if self.MODEL == "gpt-4":
            cost_per_1k_tokens_prompt = 0.03
            cost_per_1k_tokens_completion = 0.06
        elif self.MODEL == "gpt-3.5-turbo":
            cost_per_1k_tokens_prompt = 0.002
            cost_per_1k_tokens_completion = 0.002
        
        cost = (self.prompt_tokens/1000*cost_per_1k_tokens_prompt) + (self.completion_tokens/1000*cost_per_1k_tokens_completion)
        cost = round(cost, 2)  # Round the cost to 2 decimal places
        return cost

    def generate_summary(self, code_to_summarize: str):
        system_prompt = "You are a world-class software architect and developer required to summarize code using the minimum text required so that another world-class software architect and developer will be able to reconstruct the functionality entirely. You give your output in the following example format:\nFile Summary: xxx\nList of file methods: xxx\n\nWhere it is not obvious from a method name what it is doing, please include a summary of the method in the file summary.\n\nYou do not care about UI layout so if the functionality of a file is entirely related to UI layout then you do not have to list any methods and can just say \"No functional requirements, only UI\". If just one method is UI-related then you can list the method but just say \"Only UI\" for the summary"
        
        user_prompt = "Please summarize the following code:\n" + code_to_summarize
        
        gpt_message = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        try:
            response = openai.ChatCompletion.create(
                model=self.MODEL,
                messages=gpt_message,
                max_tokens=2048,
                temperature=0,
            )

            # extract the response content
            print(response)
            response_content = response['choices'][0]['message']['content'].strip()
            self.prompt_tokens+=response['usage']['prompt_tokens']
            self.completion_tokens+=response['usage']['completion_tokens']

            return response_content

        except Exception as error:
            raise error