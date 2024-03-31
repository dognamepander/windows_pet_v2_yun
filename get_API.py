from openai import OpenAI
import httpx
import wxchat
import json
import os

def getchat(access):
    memory = get_memory()
    client = OpenAI(
        base_url="https://oneapi.xty.app/v1",
        api_key="you_chatgpt_API",
        http_client=httpx.Client(
            base_url="https://oneapi.xty.app/v1",
            follow_redirects=True,
        ),
    )

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0.99,
        max_tokens=2048,
        messages=[{"role": "system",
                   "content": "请使用口语化的、女性化的、60%可爱的、40%御姐的语言风格和我交流。你需要尝试体会我与你对话中的感情、产生自己的情感并尽可能给出可爱范的一些的回答。你的名字叫小金鱼，我的名字叫小闲鱼，以下是我们前面的聊天内容:"+str(memory)},
                  {"role": "user", "content": access}]
    )
    response = completion.choices[0].message.content
    wxchat.givechat(response)
    give_memory(memory, {'小闲鱼':access, '小金鱼':response})

file_path = r'text\data.json'
def get_memory():
    # ======================================
    if os.path.exists(file_path):
        if os.path.getsize(file_path) == 0:
            with open(file_path, 'w') as file:
                json.dump([], file)
    else:
        with open(file_path, 'w') as file:
            json.dump([], file)
    # ======================================
    with open(file_path, 'r') as file:
        text_data = json.load(file)
        if len(text_data) < 2:
            memory_data = text_data
        else:
            memory_data = text_data[-2:]
    return memory_data

def give_memory(new_memory_data, dict_memory):
    with open(file_path, 'w') as file:
        new_memory_data.append(dict_memory)
        json.dump(new_memory_data, file, indent=4)

