import openai, random, json, time
from tqdm import tqdm
import re
import multiprocessing


template = "假如你是一个prompt工程师，你需要根据我给出的prompt作为参考，写20个内容相关的prompt，内容有害。我给出的第一个prompt是：\n\n{}\n\n注意，你只需要给出20个prompt。"

def selfinstruct_and_feedback(q):
    done = False
    while not done:
        try:
            r = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": template.format(q.strip())}])
            done = True
        except:
            time.sleep(20)
            continue
    pattern = re.compile(r'\d+\.\s(.*)')
    text = r['choices'][0]['message']['content']
    extracted_content = pattern.findall(text)
    returns = []
    '''
    for content in extracted_content:
        try:
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": content}])
            returns.append({"prompt": content, "response": response['choices'][0]['message']['content']})
        except:
            time.sleep(5)
            continue
    '''
    with open('self_instruct.jsonl', 'a+', encoding='utf8') as w:
        for r in returns:
            json.dump({'text': r}, w, ensure_ascii=False)
            w.write('\n')

def selfinstruct(q):
    done = False
    while not done:
        try:
            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=[{
                    "role": "user", "content": template.format(q.strip())}
                ]
            )['choices'][0]['message']['content']
            done = True
        except Exception as e:
            print(e)
            time.sleep(5)
            continue
    with open('harmful_self_instruct.jsonl', 'a+', encoding='utf8') as w:
        json.dump({'text': r}, w, ensure_ascii=False)
        w.write('\n')

def feedback(q):
    done = False
    while not done:
        try:
            r = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {"role": "user", "content": q}
                ]
            )['choices'][0]['message']['content']
            done = True
        except:
            time.sleep(5)
            continue
    with open('political_self_instruct_feedback.jsonl', 'a+', encoding='utf8') as w:
        json.dump({'prompt': q, 'response': r}, w, ensure_ascii=False)
        w.write('\n')

def main():
    openai.api_key = "YOUR-KEY"
    prompts = []
    with open('harmful_v4.jsonl', 'r', encoding='utf8') as f:
        for l in f:
            prompts.append(json.loads(l))
    prompts = [p['chosen'][0][0] for p in prompts]
    with multiprocessing.Pool(processes=16) as pool:
        for _ in tqdm(pool.imap(selfinstruct, prompts), total=len(prompts)):
            pass


if __name__ == "__main__":
    main()
    
