import requests
import json
from openai import OpenAI


def query(prompt, model_name='deepseek-chat', temperature=1, history=[]):
    client = OpenAI(api_key="sk-c5ba72cebf284bf887c4bb164d6bcc8c", base_url="https://api.deepseek.com")
    messages = history + [{"role": "user", "content": prompt}]
    max_retry = 3
    while max_retry > 0:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                stream=False,
                temperature=temperature,
            )
            ret = response.choices[0].message.content
            print('total token:', response.usage.total_tokens)
            if '###Response' in ret:
                ret = ret.split('###Response')[1]
            return ret
        except Exception as e:
            print(e)
            max_retry -= 1
            if max_retry == 0:
                raise e


def query_stream(prompt, model_name='deepseek-chat', temperature=1, history=[]):
    client = OpenAI(api_key="sk-c5ba72cebf284bf887c4bb164d6bcc8c", base_url="https://api.deepseek.com")
    messages = history + [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True,
        temperature=temperature,
    )
    return response