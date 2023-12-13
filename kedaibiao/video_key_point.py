

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

from tqdm import tqdm
from multiprocessing import Process, Manager
import multiprocessing

from collections import OrderedDict

data_list = []
with open('/home/htxu91/video_key_point/eval_latest_all.json') as frobj:
    for line in frobj:
        try:
            d = json.loads(line.strip())
            data_list.append(d)
        except:
            continue
d_dict = {}
for d in data_list:
    if d['v2_first_tag_name'] not in d_dict:
        d_dict[d['v2_first_tag_name']] = []
    d_dict[d['v2_first_tag_name']].append(d)

template = []
with open('/home/htxu91/video_key_point/视频要点总结.jsonl') as frobj:
    for line in frobj:
        d = json.loads(line.strip())
        d = f"example0: \ninput: \n{d['input']}\noutput:\n{d['output']}"
        template.append(d)

def multi_process(data_dict,
                output_file,
                random_seed=2018):

    num_of_documents = len(data_dict)
    print('==num_of_documents==', num_of_documents)

    pool = multiprocessing.Pool(processes=num_of_documents)

    for chunk_id, key in enumerate(list(data_dict.keys())):
        output_file_ = output_file + "/video_key_point_v2_{}.{}".format(key, chunk_id)
        pool.apply_async(generate_fn,
            args=(data_dict, key, output_file_)) # apply_async

    pool.close()
    pool.join()
                
def build_index_chunk(num_of_documents, process_num):
    

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

import re
from tqdm import tqdm
import random
def generate_fn(d_dict, key, output_file_):
    with open(output_file_, 'w') as fwobj:
        d_list = d_dict[key]
        for idx in tqdm(range(len(d_list))):
            d = d_list[idx]
            if 'new_asr' not in d:
                continue
            if 'asr_text' not in d['new_asr']:
                continue
                
            random_key = np.random.choice(key_list)
            openai.api_key = random_key
    
            seed = random.choice(template)
            time.sleep(1)
            output_list = []
            for _ in range(5):
                seed = random.choice(template)
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4-1106-preview", 
                        messages=[{"role": "system", "content": seed},
                      {'role':'user', "content": f"example1: \ninput:\nASR: {d['asr_时间戳']}\noutput:\n"}],
                                    temperature=0.7,
                                    presence_penalty=0.0,
                                    top_p=1.0,
                                    frequency_penalty=0.0,
                                    max_tokens=2048)
                    response_passage = response['choices'][0]['message']['content']
                    output_list.append({
                        'template': seed,
                        'response': response_passage
                    })
                    continue
                except:
                    response_passage = ''
                    continue
                
            d['key_summary'] = {
                'system': seed,
                'response': output_list
            }
            fwobj.write(json.dumps(d, ensure_ascii=False)+'\n')
            # break
            
output_file = '/home/htxu91/video_key_point_latest'
# generate_fn(d_dict, '三农', '/home/htxu91/video_key_point/test.jsonl')
multi_process(d_dict,
                output_file,
                random_seed=2018)
