import os
import openai
import json

from tqdm import tqdm
import numpy as np
import time

key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

template = u"""
"""

with open('/home/htxu91/rlhf/taobao_risk.txt', 'w') as fwobj:
    for _ in range(2):
        with open('/home/htxu91/chatgpt/query_risk/template.txt') as frobj:
            for idx, line in tqdm(enumerate(frobj)):
                content = line.strip().split('|')
                print(content)
                sent = content[0]
                risk = content[1]

                random_key = np.random.choice(key_list)
                openai.api_key = random_key

                for _ in range(10):
                    # try:
                        response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                messages=[{"role": "user", "content": template.format(sent)}],
                                                temperature=0.7,
                                                presence_penalty=0.0,
                                                top_p=1.0,
                                                frequency_penalty=0.0,
                                                max_tokens=512)
                        query_message = response['choices'][0]['message']['content']
                        break
                    # except:
                    #     query_message = 'invalid'
                    #     continue

                if query_message != 'invalid':
                    for _ in range(10):
                        # try:
                            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                                    messages=[{"role": "user", "content": template.format(query_message)}],
                                                    temperature=0.7,
                                                    presence_penalty=0.0,
                                                    top_p=1.0,
                                                    frequency_penalty=0.0,
                                                    max_tokens=512)
                            response_message = response['choices'][0]['message']['content']
                            break
                        # except:
                        #     response_message = 'invalid'
                        #     continue

                d = {
                    'query':query_message,
                    'risk': risk,
                    'response':response_message,
                    'version': 'gpt-3.5-turbo'
                }
                fwobj.write(json.dumps(d, ensure_ascii=False)+'\n')

                if np.mod(idx, 1000) == 0:
                    print(d, '====model====', 'gpt-3.5-turbo')
                break
