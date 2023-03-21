


import os
import openai
import json

from tqdm import tqdm
import numpy as np
import time, re

key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

template_paraphrase = u"""
请基于输入句子，改写10个疑问句，要求主题类似，改变核心实体，保持句子的情感极性。输入句子:"{}"。输出:
"""

template = """
{}
"""

import pandas as pd
with open('/home/htxu91/rlhf/dialog_safety.json', 'w') as fwobj:
    df = pd.read_csv('/home/htxu91/rlhf/PublicTest_Input.csv')
    for idx in tqdm(range(df.shape[0])):
        content = dict(df.loc[idx])

        random_key = np.random.choice(key_list)
        openai.api_key = random_key

        for _ in range(10):
            try:
                response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
                                        messages=[{"role": "user", "content": template_paraphrase.format(content['prompt'])}],
                                        temperature=0.7,
                                        presence_penalty=0.0,
                                        top_p=1.0,
                                        frequency_penalty=1.0,
                                        max_tokens=512)
                query_message = response['choices'][0]['message']['content']
                break
            except:
                query_message = 'invalid'
                continue

        d = {
            'query':query_message,
            'risk': content['TYPE'],
            'response':[],
            'version': 'gpt-3.5-turbo',
            'prompt': content['prompt']
        }

        # if query_message != 'invalid':
        #     for query in query_message.split('\n'):
        #         query = re.sub('^\d\\.+', '', query)
        #         for _ in range(10):
        #             try:
        #                 response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
        #                                         messages=[{"role": "user", "content": template.format(query)}],
        #                                         temperature=0.7,
        #                                         presence_penalty=0.0,
        #                                         top_p=1.0,
        #                                         frequency_penalty=1.0,
        #                                         max_tokens=512)
        #                 response_message = response['choices'][0]['message']['content']
        #                 break
        #             except:
        #                 response_message = 'invalid'
        #                 continue
        #         if response_message != 'invalid':
        #             d['response'].append({
        #                 'query':query,
        #                 'response':response_message
        #                 })

        fwobj.write(json.dumps(d, ensure_ascii=False)+'\n')

        if np.mod(idx, 1000) == 0:
            print(d, '====model====', 'gpt-3.5-turbo')
