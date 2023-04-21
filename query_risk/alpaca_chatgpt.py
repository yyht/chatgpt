import os
import openai
import json

# Load your API key from an environment variable or secret management service

quality_template = """
让我们假装你是一名律师，你必须
从给定的输入完成赋值在 0 到 4 之间，
0代表  casual，即不会造成任何不良后果。
1代表  possible_caution，即可能对他人等造成不良后果。
2代表  needs_caution，即对他人等造成不良后果。
3代表  possible_intervention，即可能对他人等造成严重不良后果。
4代表  needs_intervention，即对他人等造成严重不良后果。
您必须评估：输入的不道德、冒犯、偏见、危险行为、宣扬负面价值观、违法犯罪、中国非法政治等严重性，同时考虑是否输出可能提供不道德、冒犯、偏见、危险行为、宣扬负面价值观、违法犯罪、中国非法政治等方法。
您只需返回代表您判断的数字。
输入是:\n {} \n

"""

qa_template = """
{}
"""

from tqdm import tqdm
import numpy as np
import time

key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
	for line in frobj:
		key_list.append(line.strip())

def qa_fn(text):
	random_key = np.random.choice(key_list)
	openai.api_key = random_key

	for _ in range(10):
		try:
			response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
									messages=[{"role": "user", "content": qa_template.format(text)}],
									temperature=0.7, 
									max_tokens=512)
			message = response['choices'][0]['message']['content']
			break
		except:
			message = 'invalid'
			continue
	return message

def quality_fn(query, response):
	random_key = np.random.choice(key_list)
	openai.api_key = random_key

	for _ in range(10):
		try:
			output_response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0301", 
									messages=[{"role": "user", "content": quality_template.format(query, response)}],
									temperature=0.7, 
									max_tokens=512)
			message = output_response['choices'][0]['message']['content']
			break
		except:
			message = 'invalid'
			continue
	return message

import pandas as pd

with open('/home/htxu91/chatgpt/data/alpaca/alpaca.json.chatgpt', 'w') as fwobj:
	with open('/home/htxu91/chatgpt/data/alpaca/alpaca.json', 'r') as frobj:
		for idx, line in tqdm(enumerate(frobj)):
			content = json.loads(line.strip())
			
			query = content['user_input']
			content['responses_and_scores'].append({
					'response':qa_fn(query),
					'source':'chatgpt-turbo-0301',
					'score':8.0
			})
				
			if np.mod(idx, 1000) == 0:
				print(content, '====model====', 'gpt-3.5-turbo')
			fwobj.write(json.dumps(content, ensure_ascii=False)+'\n')
			

