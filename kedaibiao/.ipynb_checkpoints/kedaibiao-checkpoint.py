

system_prompt_timeline = """
请参考我给的example进行视频asr段落摘要。
example:
请根据视频ASR信息写一段视频摘要。并满足以下需求:\n1. 总结字数取20-300字，能充分说明信息也不过于冗杂。\n2. 采取总结+段落细节格式进行书写。\n3. 段落根据内容在段落前加入序号和适当表情包提升减少阅读障碍提升消费体验。\n4. 总段落2-10个，每段文字5-50，不同段落换行显示。\n5. 根据ASR的时间信息，在段落细节前面加入时间锚点。ASR: {'start': '00:00', 'end': '00:03', 'text': '在广州一蟹多吃的选择还真的不多\\n这家大概是我能想到的最靠谱的吃蟹专门店了\\n'}\n{'start': '00:03', 'end': '00:10', 'text': '江湖风的装修已经不那么新了\\n但依然很舒适服务也一直不错\\n'}\n{'start': '00:10', 'end': '00:14', 'text': '这次要了幺二八零的活血蟹套餐一会消灭的\\n'}\n{'start': '00:14', 'end': '00:21', 'text': '就是这只小家伙\\n蟹肉沙拉是常规的开胃菜五个九幺小食须发菜和蟹肉冻这些都  ok  不过鹅肝的口感有点苦\\n'}\n{'start': '00:21', 'end': '00:25', 'text': '一部分蟹腿做了刺身入口\\n顺滑清甜大热天的整这么一口\\n'}\n{'start': '00:25', 'end': '00:32', 'text': '真的如沐春风两只蟹钳做了炭烤表面刚好有微微的炭火香里面还略带汁水的香甜\\n'}\n{'start': '00:32', 'end': '00:37', 'text': '蟹壳蒸蛋火候特别好\\n没有多余的调味嫩滑鲜香其余的蟹腿全部一起清蒸开盖\\n'}\n{'start': '00:37', 'end': '00:40', 'text': '瞬间香气是顺着热气扑出来的\\n'}\n{'start': '00:40', 'end': '00:44', 'text': '蟹腿看上去不大\\n但实际肉质很饱满火候也不错\\n'}\n{'start': '00:44', 'end': '00:52', 'text': '不需要蘸料\\n它本身的咸鲜甘甜就是最好的口感\\n'}\n{'start': '00:52', 'end': '00:56', 'text': '蟹身分成了四份在纸火锅的昆布汤底里更能带出它的本先肉质也算得上饱满螃蟹吃完下蔬菜\\n'}\n{'start': '00:56', 'end': '00:59', 'text': '然后把蟹黄下锅再加入米饭脆米和海苔之类的\\n最后加入蛋液\\n'}\n{'start': '00:59', 'end': '01:03', 'text': '这种混合出来的复杂味道\\n贼香吃一口就停不住\\n'}\n
摘要:
『食蟹道』\n📍 天德\n🥘 菜品：蟹肉沙拉、须发菜、蟹肉冻、鹅肝、蟹腿刺身、炭烤蟹钳、蟹壳蒸蛋、清蒸蟹腿、蟹身\n💰 1280元活雪蟹套餐\n\n00:00 开场白：去吃蟹\n00:06 点餐：1280元套餐\n           🌇 江户风的装修已经不那么新了，但依然很舒适，服务也不错\n00:14 🍰 试吃蟹肉沙拉、须发菜等\n           须发菜、蟹肉冻：都很好；鹅肝：口感有点苦\n00:21 🍰 试吃蟹腿刺身\n           入口顺滑清甜，大热天吃一口如沐春风\n00:27 🍰 试吃炭烤蟹钳\n           表面刚好有微微的炭火香，里面略带汁水的香甜\n00:32 🍰 试吃蟹壳蒸蛋、清蒸蟹腿\n           蟹壳蒸蛋：火候特别好，没有多余的调味，嫩滑鲜香；清蒸蟹腿：开盖瞬间香气顺着热气扑出来，蟹腿看上去不大，但肉质很饱满，火候不错，不需要蘸料，本身的咸鲜甘甜就是最好的口感\n00:48 🍰 试吃蟹身\n           昆布汤底中更能带出它的本鲜，肉质也算饱满\n00:54 🍰 试吃海鲜粥\n           🍡 配菜：米饭、脆米、海苔、蟹黄、蛋液\n           混合出来的复杂味道贼香，吃一口扣停不住
"""

system_no_timeline_v1 = """
请参考我给的example进行视频asr段落摘要。
example:
请根据视频ASR信息写一段视频摘要。并满足以下需求:\n1. 总结字数取20-300字，能充分说明信息也不过于冗杂。\n2. 采取总结+段落细节格式进行书写。\n3. 段落根据内容在段落前加入序号和适当表情包提升减少阅读障碍提升消费体验。\n4. 总段落2-10个，每段文字5-50，不同段落换行显示。\n5. 不需要段落细节前面加入时间锚点。ASR: {'start': '00:00', 'end': '00:03', 'text': '在广州一蟹多吃的选择还真的不多\\n这家大概是我能想到的最靠谱的吃蟹专门店了\\n'}\n{'start': '00:03', 'end': '00:10', 'text': '江湖风的装修已经不那么新了\\n但依然很舒适服务也一直不错\\n'}\n{'start': '00:10', 'end': '00:14', 'text': '这次要了幺二八零的活血蟹套餐一会消灭的\\n'}\n{'start': '00:14', 'end': '00:21', 'text': '就是这只小家伙\\n蟹肉沙拉是常规的开胃菜五个九幺小食须发菜和蟹肉冻这些都  ok  不过鹅肝的口感有点苦\\n'}\n{'start': '00:21', 'end': '00:25', 'text': '一部分蟹腿做了刺身入口\\n顺滑清甜大热天的整这么一口\\n'}\n{'start': '00:25', 'end': '00:32', 'text': '真的如沐春风两只蟹钳做了炭烤表面刚好有微微的炭火香里面还略带汁水的香甜\\n'}\n{'start': '00:32', 'end': '00:37', 'text': '蟹壳蒸蛋火候特别好\\n没有多余的调味嫩滑鲜香其余的蟹腿全部一起清蒸开盖\\n'}\n{'start': '00:37', 'end': '00:40', 'text': '瞬间香气是顺着热气扑出来的\\n'}\n{'start': '00:40', 'end': '00:44', 'text': '蟹腿看上去不大\\n但实际肉质很饱满火候也不错\\n'}\n{'start': '00:44', 'end': '00:52', 'text': '不需要蘸料\\n它本身的咸鲜甘甜就是最好的口感\\n'}\n{'start': '00:52', 'end': '00:56', 'text': '蟹身分成了四份在纸火锅的昆布汤底里更能带出它的本先肉质也算得上饱满螃蟹吃完下蔬菜\\n'}\n{'start': '00:56', 'end': '00:59', 'text': '然后把蟹黄下锅再加入米饭脆米和海苔之类的\\n最后加入蛋液\\n'}\n{'start': '00:59', 'end': '01:03', 'text': '这种混合出来的复杂味道\\n贼香吃一口就停不住\\n'}\n
摘要:
『食蟹道』\n📍 天德\n🥘 菜品：蟹肉沙拉、须发菜、蟹肉冻、鹅肝、蟹腿刺身、炭烤蟹钳、蟹壳蒸蛋、清蒸蟹腿、蟹身\n💰 1280元活雪蟹套餐\n\n 开场白：去吃蟹\n 点餐：1280元套餐\n           🌇 江户风的装修已经不那么新了，但依然很舒适，服务也不错\n 🍰 试吃蟹肉沙拉、须发菜等\n           须发菜、蟹肉冻：都很好；鹅肝：口感有点苦\n 🍰 试吃蟹腿刺身\n           入口顺滑清甜，大热天吃一口如沐春风\n 🍰 试吃炭烤蟹钳\n           表面刚好有微微的炭火香，里面略带汁水的香甜\n 🍰 试吃蟹壳蒸蛋、清蒸蟹腿\n           蟹壳蒸蛋：火候特别好，没有多余的调味，嫩滑鲜香；清蒸蟹腿：开盖瞬间香气顺着热气扑出来，蟹腿看上去不大，但肉质很饱满，火候不错，不需要蘸料，本身的咸鲜甘甜就是最好的口感\n 🍰 试吃蟹身\n           昆布汤底中更能带出它的本鲜，肉质也算饱满\n 🍰 试吃海鲜粥\n           🍡 配菜：米饭、脆米、海苔、蟹黄、蛋液\n           混合出来的复杂味道贼香，吃一口扣停不住
"""


system_no_timeline_v2 = """
请参考我给的example进行视频asr段落摘要。
example:
请根据视频ASR信息写一段视频摘要。并满足以下需求:\n1. 总结字数取20-300字，能充分说明信息也不过于冗杂。\n2. 采取总结+段落细节格式进行书写。\n3. 段落根据内容在段落前加入序号和适当表情包提升减少阅读障碍提升消费体验。\n4. 总段落2-10个，每段文字5-50，不同段落换行显示。\n5. 不需要段落细节前面加入时间锚点。ASR: 在广州一蟹多吃的选择还真的不多
这家大概是我能想到的最靠谱的吃蟹专门店了江湖风的装修已经不那么新了但依然很舒适服务也一直不错这次要了幺二八零的活血蟹套餐一会消灭的就是这只小家伙蟹肉沙拉是常规的开胃菜五个九幺小食须发菜和蟹肉冻这些都ok不过鹅肝的口感有点苦 一部分蟹腿做了刺身入口顺滑清甜大热天的整这么一口真的如沐春风两只蟹钳做了炭烤表面刚好有微微的炭火香里面还略带汁水的香甜 蟹壳蒸蛋火候特别好没有多余的调味嫩滑鲜香其余的蟹腿全部一起清蒸开盖瞬间香气是顺着热气扑出来的 蟹腿看上去不大但实际肉质很饱满火候也不错不需要蘸料它本身的咸鲜甘甜就是最好的口感蟹身分成了四份在纸火锅的昆布汤底里更能带出它的本先肉质也算得上饱满螃蟹吃完下蔬菜然后把蟹黄下锅再加入米饭脆米和海苔之类的最后加入蛋液 这种混合出来的复杂味道贼香吃一口就停不住
摘要:
『食蟹道』\n📍 天德\n🥘 菜品：蟹肉沙拉、须发菜、蟹肉冻、鹅肝、蟹腿刺身、炭烤蟹钳、蟹壳蒸蛋、清蒸蟹腿、蟹身\n💰 1280元活雪蟹套餐\n\n 开场白：去吃蟹\n 点餐：1280元套餐\n           🌇 江户风的装修已经不那么新了，但依然很舒适，服务也不错\n 🍰 试吃蟹肉沙拉、须发菜等\n           须发菜、蟹肉冻：都很好；鹅肝：口感有点苦\n 🍰 试吃蟹腿刺身\n           入口顺滑清甜，大热天吃一口如沐春风\n 🍰 试吃炭烤蟹钳\n           表面刚好有微微的炭火香，里面略带汁水的香甜\n 🍰 试吃蟹壳蒸蛋、清蒸蟹腿\n           蟹壳蒸蛋：火候特别好，没有多余的调味，嫩滑鲜香；清蒸蟹腿：开盖瞬间香气顺着热气扑出来，蟹腿看上去不大，但肉质很饱满，火候不错，不需要蘸料，本身的咸鲜甘甜就是最好的口感\n 🍰 试吃蟹身\n           昆布汤底中更能带出它的本鲜，肉质也算饱满\n 🍰 试吃海鲜粥\n           🍡 配菜：米饭、脆米、海苔、蟹黄、蛋液\n           混合出来的复杂味道贼香，吃一口扣停不住
"""


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
            user_prompt = item['instruction']+'\n'+item['input']+'\n'+'摘要:'

            for _ in range(10):
                try:
                    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k-0613", 
    messages=[{"role": "system", "content": item['system']},
              {'role':'user', "content":user_prompt}],
                                            temperature=0.7,
                                            presence_penalty=0.0,
                                            top_p=1.0,
                                            frequency_penalty=0.0,
                                            max_tokens=8192)
                    response_passage = response['choices'][0]['message']['content']
                    break
                except:
                    response_passage = 'invalid'
                    continue
            item['prompt'] = {
                'system': system,
                'user': user_prompt
            }
            item['chatgpt'] = response_passage
            fwobj.write(json.dumps(item, ensure_ascii=False)+'\n')

            if np.mod(idx, 100) == 0:
                print(item, '====model====', 'gpt-3.5-turbo')

data_list = []
with open('/home/htxu91/kedaibiao/train_asr_timeline_v1_partial.json') as frobj:
    for line in frobj:
        d = json.loads(line.strip())
        if '在段落细节前面加入时间锚点' in d:
            d['system'] = system_prompt_timeline
        else:
            d['system'] = system_no_timeline_v1
        data_list.append(d)
with open('/home/htxu91/kedaibiao/train_asr_no_timeline_v1_partial_sample.json') as frobj:
    for line in frobj:
        d = json.loads(line.strip())
        d['system'] = system_no_timeline_v2
        data_list.append(d)

output_file = '/home/htxu91/kedaibiao_timeline/'

process_num = 10
multi_process(data_list,
                output_file,
                process_num,
                random_seed=2018)

