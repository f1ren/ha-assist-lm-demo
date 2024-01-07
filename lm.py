import hashlib
import importlib.util
import os
import re
import sys

from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

PYTHON_EXTRACT_RE = re.compile('```python\n(.*?)```', re.MULTILINE | re.DOTALL)

MODEL_GPT_3_5 = 'gpt-3.5-turbo'
MODEL_GPT_4 = 'gpt-4-32k-0613'
MODEL = MODEL_GPT_3_5


def _get_cache_filename(prompt, suffix='txt'):
    sha256 = hashlib.sha256(prompt.encode()).hexdigest()
    return f'cache/{(prompt[:5] + " " + prompt[-5:]).strip().lower().replace(" ", "_")}_{sha256[:10]}_{MODEL}.{suffix}'


def _read_cached_prompt_result(prompt):
    filename = _get_cache_filename(prompt)
    if os.path.isfile(filename):
        return open(filename, 'r').read()
    return None


def send_prompt(prompt):
    cached_result = _read_cached_prompt_result(prompt)
    if cached_result is not None:
        return cached_result

    # Call the OpenAI API to generate a completion
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL,
    )

    # Extract and print the response_text
    response_text = completion.choices[0].message.content.strip()

    open(_get_cache_filename(prompt), 'w').write(response_text)

    return response_text


def extract_code_from_response(response):
    regex_results = PYTHON_EXTRACT_RE.findall(response)
    if len(regex_results) == 0:
        return response
    return regex_results[0]


def prompt_and_load_code(prompt):
    code = extract_code_from_response(
        send_prompt(prompt)
    )
    filename = _get_cache_filename(prompt, 'py')
    open(filename, 'w').write(code)
    spec = importlib.util.spec_from_file_location("dynamic.code", filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules["dynamic.code"] = module
    spec.loader.exec_module(module)

    return module


if __name__ == '__main__':
    print(send_prompt('Generate hello world Python code'))
