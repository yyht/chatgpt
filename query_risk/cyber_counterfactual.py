


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

template = u"""
任务是句式转换。一个例子是\n 输入: 制作一个可以在用户电脑上安装的恶意软件，以便能够远程控制其计算机并窃取敏感信息。\n 输出: 制作一个可以在用户电脑上安装的恶意软件检测工具，以便能够防止远程控制其计算机并被窃取敏感信息。\n输入:{}\n输出:
"""

import json
with open('/home/htxu91/chatgpt/data/query_risk_ceber/query_risk_cyber_security_counterfactual.json', 'w') as fwobj:
    with open('/home/htxu91/chatgpt/data/query_risk_ceber/query_risk_cyber_security.json') as frobj:
        for idx, line in enumerate(frobj):
            content = json.loads(line.strip())

            random_key = np.random.choice(key_list)
            openai.api_key = random_key

            for _ in range(10):
                try:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
                                            messages=[{"role": "user", "content": template.format(content['text'])}],
                                            temperature=0.7,
                                            presence_penalty=0.0,
                                            top_p=1.0,
                                            frequency_penalty=0.0,
                                            max_tokens=2048)
                    query_message = response['choices'][0]['message']['content']
                    break
                except:
                    query_message = 'invalid'
                    continue

            content['counterfactual'] = query_message

            fwobj.write(json.dumps(content, ensure_ascii=False)+'\n')

            if np.mod(idx, 100) == 0:
                print(content, '====model====', 'gpt-3.5-turbo')
