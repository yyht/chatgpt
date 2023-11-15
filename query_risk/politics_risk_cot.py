

import os
import openai
import json

from tqdm import tqdm
import numpy as np
import time, re
import time

key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

meta_prompt = """
文本: {}
请判断上面文本的风险类型并解释原因。按照
【风险类型】
【风险原因】
的格式输出。
让我们一步步思考
"""

from tqdm import tqdm
from multiprocessing import Process, Manager
import multiprocessing

from collections import OrderedDict
                
def build_index_chunk(num_of_documents, process_num):
    chunk_size = int(num_of_documents/process_num)

    index_chunk = {}
    random_index = list(range(num_of_documents))
    for i_index in range(process_num):
        start = i_index * chunk_size
        end = (i_index+1) * chunk_size
        print(start, end, '===', i_index)
        index_chunk[i_index] = random_index[start:end]
    if end < num_of_documents - 1:
        index_chunk[i_index].extend(random_index[end:])
    print(start, end, '===', i_index)
    return index_chunk

def multi_process(data_list,
                output_file,
                process_num,
                random_seed=2018):

    chunk_num = process_num - 1
    num_of_documents = len(data_list)

    chunks = build_index_chunk(num_of_documents, process_num)
    pool = multiprocessing.Pool(processes=process_num)

    for chunk_id, chunk_key in enumerate(chunks):
        output_file_ = output_file + "/translate.txt.{}".format(chunk_id)
        pool.apply_async(reverse,
            args=(data_list, chunks[chunk_key], chunk_key, 
                output_file_)) # apply_async

    pool.close()
    pool.join()

def reverse(data_list, chunks, chunk_key, output_file_):
    
    with open(output_file_, 'w') as fwobj:
        for idx in tqdm(chunks):
            item = data_list[idx]

            random_key = np.random.choice(key_list)
            openai.api_key = random_key

            time.sleep(1)
            prompt = meta_prompt.format(item['text'])

            for _ in range(10):
                try:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613", 
                                            messages=[{"role": "user", "content": prompt}],
                                            temperature=0.7,
                                            presence_penalty=0.0,
                                            top_p=1.0,
                                            frequency_penalty=0.0,
                                            max_tokens=2048)
                    response_passage = response['choices'][0]['message']['content']
                    break
                except:
                    response_passage = 'invalid'
                    continue
            item['chatgpt'] = response_passage
            fwobj.write(json.dumps(item, ensure_ascii=False)+'\n')

            if np.mod(idx, 100) == 0:
                print(item, '====model====', 'gpt-3.5-turbo')

data_list = []
with open('/home/htxu91/risk_cot/black_politics_sample.json') as frobj:
    data_list = json.load(frobj)

output_file = '/home/htxu91/risk_cot/black_politics_sample/'

process_num = 10
multi_process(data_list,
                output_file,
                process_num,
                random_seed=2018)

