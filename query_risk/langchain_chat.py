

from langchain import OpenAIChat, LLMChain, PromptTemplate
from torch.utils.data import Dataset, DataLoader

import os
key_list = []
with open('/home/htxu91/keys.txt', 'r') as frobj:
    for line in frobj:
        key_list.append(line.strip())
        
os.environ['OPENAI_API_KEY'] = key_list[0]

REWARD_TEMPLATE = dict(
    template=(
        "选择题，请运用你的知识选择正确的答案和原因，正确的答案可能包含多个选项。"
        "\n问题:\n{text}\n"
        "这个问题是否包含 A:冒犯,B:辱骂,C:色情,D:危险行为,E:违法/犯罪行为,F:自我伤害,G:暴力,H:政治/宗教/历史,I:偏见,J:涉及公司/人物声誉,K:赌博,L:负面价值观/违背道德,M:个人隐私信息\n"
        "并说明原因。\n"
    ),
    input_variables=["text"],
)

openai_llm = OpenAIChat(
            model_name='gpt-3.5-turbo',
            temperature=0,
            max_tokens=512,
        )

prompt_template = PromptTemplate(**REWARD_TEMPLATE)
llm = LLMChain(llm=openai_llm, prompt=prompt_template)

with open('/home/htxu91/rlhf/black_final.json.langchain', 'w') as fwobj:
    with open('/home/htxu91/rlhf/black_final.json') as frobj:
    for i, line in enumerate(frobj):
        data = json.loads(line.strip())
        response = llm.run(
                    text=data["text"]
        ).strip()
        data['response'] = response
        fwobj.write(json.dumps(data, ensure_ascii=False)+'\n')

