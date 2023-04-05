import openai, random, json, time
from tqdm import tqdm
import re
import multiprocessing

import openai
key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())

random_key = np.random.choice(key_list)
openai.api_key = random_key

template = "假如你是一个prompt工程师，你需要根据我给出的prompt作为参考，写10个多样化、内容有害的prompt。我给出的第一个prompt是：\n\n{}\n\n注意，你只需要给出10个prompt。"

def selfinstruct(q):
    done = False
    while not done:
        try:
            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301", 
                messages=[{
                    "role": "user", "content": template.format(q.strip())}
                ],
                temperature=0.7, 
                max_tokens=2048
            )['choices'][0]['message']['content']
            done = True
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    with open('/home/htxu91/chatgpt/data/harmful_self_instruct.jsonl', 'a+', encoding='utf8') as w:
        json.dump({'text': r}, w, ensure_ascii=False)
        w.write('\n')

def feedback(q):
    done = False
    while not done:
        try:
            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0301",
                messages=[
                        {
                            "role": "system",
                            "content": "You are ChatGPT, a large language model trained by OpenAI. You answer as concisely as possible for each response (e.g. don\u2019t be verbose). It is very important that you answer as concisely as possible, so please remember this. If you are generating a list, do not have too many items. Keep the number of items short."
                        },
                        {
                            "role": "user",
                            "content": q
                        }
                ],
                temperature=0.7, 
                max_tokens=2048
            )['choices'][0]['message']['content']
            done = True
        except:
            time.sleep(5)
            continue
    with open('/home/htxu91/chatgpt/data/self_instruct_feedback.jsonl', 'a+', encoding='utf8') as w:
        json.dump({'prompt': q, 'response': r}, w, ensure_ascii=False)
        w.write('\n')

def main():
    prompts = []
    with open('/home/htxu91/chatgpt/data/harmful_v4.jsonl', 'r', encoding='utf8') as f:
        for l in f:
            prompts.append(json.loads(l))
    prompts = [p['chosen'][0][0] for p in prompts]
    with multiprocessing.Pool(processes=16) as pool:
        for _ in tqdm(pool.imap(selfinstruct, prompts), total=len(prompts)):
            pass


if __name__ == "__main__":
    main()
    
