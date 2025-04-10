import requests
import json
from loguru import logger
from config import zhipu_key

sentences = ["This is an example sentence", "Each sentence is converted"]

from zhipuai import ZhipuAI

client = ZhipuAI(api_key=zhipu_key)

def api_encode(data_input, max_batch_size=2):
    # print('get embedding...')
    result = []
    for i in range(0, len(data_input), max_batch_size):
        cur_data = [d[:3072] for d in data_input[i:i+max_batch_size]]
        resp = client.embeddings.create(
            model="embedding-3",
            input=cur_data
        )
        if max_batch_size > 8:
            print(i)
        result += [d.embedding for d in resp.data]
    return result

if __name__ == '__main__':
    res = api_encode(sentences)
    print(len(res[0]))