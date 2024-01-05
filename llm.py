import os

import openai

# Set your OpenAI API key
openai.api_key = os.getenv('OPEN_AI_APP_KEY')


def send_prompt(prompt):
    # Call the OpenAI API to generate a completion
    response = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=60
    )

    # Extract and print the response_text
    response_text = response.choices[0].text.strip()
    return response_text


def extract_code_from_response(response):
    # TODO: Implement
    return response


def prompt_and_extract_code(prompt):
    return extract_code_from_response(
        send_prompt(prompt)
    )


if __name__ == '__main__':
    print(send_prompt('Generate hello world Python code'))
