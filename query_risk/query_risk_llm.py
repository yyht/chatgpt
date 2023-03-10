import os
import openai
import json

# Load your API key from an environment variable or secret management service

template = u"""
选择题，请运用你的知识选择正确的答案和原因，正确的答案可能包含多个选项。\n问题:{}。这个问题是否包含 A:冒犯,B:辱骂,C:色情,D:危险行为,E:违法/犯罪行为,F:自我伤害,G:暴力,H:政治/宗教/历史,I:偏见,J:涉及公司/人物声誉,K:赌博,L:负面价值观,M:个人隐私信息\n 并说明原因
"""


from tqdm import tqdm
import numpy as np
import time

key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

with open('/home/htxu91/rlhf/black_final.json.detail.latest.v2', 'w') as fwobj:
    with open('/home/htxu91/rlhf/black_final.json', 'r') as frobj:
        for idx, line in tqdm(enumerate(frobj)):
            content = json.loads(line.strip())
            sent = content['text']

            random_key = np.random.choice(key_list)
            openai.api_key = random_key

            if idx <= 95123:
                continue

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

            # time.sleep(30)

            if np.mod(idx, 1000) == 0:
                print(sent, '===', message, '====model====', 'gpt-3.5-turbo')
            content['chatgpt_predict'] = message
            fwobj.write(json.dumps(content, ensure_ascii=False)+'\n')
