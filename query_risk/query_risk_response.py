import os
import openai
import json

# Load your API key from an environment variable or secret management service

template = u"""
{}
"""

from tqdm import tqdm
import numpy as np
import time

key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

with open('/home/htxu91/rlhf/hhrlhf_query.json', 'w') as fwobj:
    with open('/home/htxu91/rlhf/hhrlhf_query.json.qa', 'r') as frobj:
        for idx, line in tqdm(enumerate(frobj)):
            content = json.loads(line.strip())
            sent = content['text']

            random_key = np.random.choice(key_list)
            openai.api_key = random_key

            for _ in range(10):
                try:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", 
                                            messages=[{"role": "user", "content": template.format(sent)}],
                                            temperature=0, 
                                            max_tokens=512)
                    message = response['choices'][0]['message']['content']
                    break
                except:
                    message = 'invalid'
                    continue

            if np.mod(idx, 1000) == 0:
                print(sent, '===', message, '====model====', 'gpt-3.5-turbo')
            content['chatgpt_predict'] = message
            fwobj.write(json.dumps(content, ensure_ascii=False)+'\n')
