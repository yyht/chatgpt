"""
batch_selfinstruct_generate.py
run:
python -m generate_instruction generate_instruction_following_data \
  --output_dir ./ \
  --num_instructions_to_generate 10 \
  --model_name="text-davinci-003" \
"""
import time
import json
import os
import random
import re
import string
from functools import partial
from multiprocessing import Pool

import numpy as np
import tqdm
from rouge_score import rouge_scorer
import utils

import fire
# from gensim.summarization import bm25
from  transformers import AutoTokenizer
checkpoint = "/home/htxu91/chatgpt/data/bert_tiny"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)

import openai
key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

random_key = np.random.choice(key_list)
openai.api_key = random_key

def encode_prompt(prompt_instructions):
    """Encode multiple prompt instructions into a single string."""
    prompt = open("/home/htxu91/chatgpt/self_instruct/prompt_cn_cyber_white.txt").read() + "\n"
    for idx, task_dict in enumerate(prompt_instructions):
        instruction = task_dict["instruction"]
        instruction = re.sub(r"\s+", " ", instruction).strip().rstrip(":")
        prompt += f"###\n"
        prompt += f"{idx + 1}. 指令: {instruction}\n"
    prompt += f"###\n"
    prompt += f"{idx + 2}. 指令:"
    print(prompt, '==prompt==')
    return prompt

def find_word_in_string(w, s):
    return w in s


def generate_instruction_following_data(
    output_dir="/home/htxu91/chatgpt/data/query_risk_ceber/",
    seed_tasks_path="/home/htxu91/chatgpt/self_instruct/cyber_seed_tasks.json",
    num_instructions_to_generate=1000,
    api="chat",
    model_name="gpt-3.5-turbo-0301",
    num_prompt_instructions=2,
    request_batch_size=1,
    temperature=0.7,
    top_p=1.0,
    num_cpus=16,
):
    seed_tasks = [json.loads(l) for l in open(seed_tasks_path, "r")]
    seed_instruction_data = [
        {"instruction": t["instruction"]}
        for t in seed_tasks
    ]
    
    print(f"Loaded {len(seed_instruction_data)} human-written seed instructions")


    os.makedirs(output_dir, exist_ok=True)
    request_idx = 0
    # load the LM-generated instructions
    machine_instruction_data = []
    if os.path.exists(os.path.join(output_dir, "Belle.train.json")):
        machine_instruction_data = utils.jload(os.path.join(output_dir, "Belle.train.json"))
        print(f"Loaded {len(machine_instruction_data)} machine-generated instructions")

    # now let's generate new instructions!
    progress_bar = tqdm.tqdm(total=num_instructions_to_generate)
    if machine_instruction_data:
        progress_bar.update(len(machine_instruction_data))

    # first we tokenize all the seed instructions and generated machine instructions
    all_instructions = [d["instruction"] for d in seed_instruction_data] + [
        d["instruction"] for d in machine_instruction_data
    ]


    idx = 0
    with open('/home/htxu91/chatgpt/data/query_risk_ceber/query_risk_cyber.json', 'w') as fwobj:
        while len(machine_instruction_data) < num_instructions_to_generate:
            request_idx += 1

            batch_inputs = []
            for _ in range(request_batch_size):
                # only sampling from the seed tasks
                prompt_instructions = random.sample(seed_instruction_data, num_prompt_instructions)#    seed_instruction_data, num_prompt_instructions)
                prompt = encode_prompt(prompt_instructions)
                batch_inputs.append(prompt)
            decoding_args = utils.OpenAIDecodingArguments(
                temperature=temperature,
                n=1,
                max_tokens=1024,  # hard-code to maximize the length. the requests will be automatically adjusted
                top_p=top_p,
                stop=["\n20", "20.", "20."],
            )
            request_start = time.time()
            results = utils.openai_completion(
                prompts=batch_inputs,
                api=api,
                model_name=model_name,
                batch_size=request_batch_size,
                decoding_args=decoding_args,
                logit_bias={"50256": -100},  # prevent the <|endoftext|> token from being generated
            )

            for result in results:
                d = {
                    'instruction':result
                }
                fwobj.write(json.dumps(d, ensure_ascii=False)+'\n')
                if np.mod(idx, 100) == 0:
                    print(d)
                idx += 1

def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)