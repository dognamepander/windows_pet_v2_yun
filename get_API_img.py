#coding=utf-8
import json
import requests
import io
import base64
from PIL import Image
from openai import OpenAI
import httpx
import wxchat
import datetime
import img_yun_API

file_path = r'text\data.json'
def get_img_memory(access):
    # ======================================
    if '照片' in access or '美照' in access or '美图' in access or '图片' in access:
        memory_data = "[{小闲鱼：给我发一张的睡前性感美照，小金鱼：一位美女穿着黑丝睡衣在床上||seductive_smile}]"
        access_img = access
    else:
        with open(file_path, 'r') as file:
            text_data = json.load(file)
            if len(text_data) < 2:
                memory_data = text_data
            else:
                memory_data = text_data[-2:]
            access_img = f"当前聊天内容：{access}，注意需要描述的画面中只有你一个主要人物（一位美女），注意在最后面加上||facial expression(英文表情)。"
    getchat_before(memory_data, access_img)

def getchat_before(memory, access):
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
                   "content": "你是一位美女，是我的女友，请根据聊天内容，陪伴我做一些事情。例子：一位美女穿着白裙在海边散步||happy，描述一下画面，注意格式||后面是英文单词，画面中只有你一个主要人物。你的名字是小金鱼，我的名字是小闲鱼，以下是我们前面的聊天内容:"+str(memory)},
                  {"role": "user", "content": access}]
    )
    response = completion.choices[0].message.content
    list_response = response.split('||')
    list_response.append('giggling')
    list_response[0] = list_response[0].replace('小金鱼', '一位美女')
    getchat(list_response[0], list_response[1])

def getchat(access, emoji):
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
                   "content": "StableDiffusion是一款利用深度学习的文生图模型，支持通过使用提示词来产生新的图像，描述要包含或省略的元素。"+
                              "下面的prompt是用来指导AI绘画模型创作图像的。它们包含了图像的各种细节，如人物的外观、背景、颜色和光线效果，以及图像的主题和风格。这些prompt的格式经常包含括号内的加权数字，用于指定某些细节的重要性或强调。例如，(masterpiece:1.5)表示作品质量是非常重要的，多个括号也有类似作用。此外，如果使用中括号，如{blue hair:white hair:0.3}，这代表将蓝发和白发加以融合，蓝发占比为0.3。"+
                              "以下是用prompt帮助AI模型生成图像的例子：masterpiece,(bestquality),highlydetailed,ultra-detailed,cold,solo,(1girl),(detailedeyes),(shinegoldeneyes),(longliverhair),expressionless,(long sleeves),(puffy sleeves),(white wings),shinehalo,(heavymetal:1.1),(metaljewelry),cross-lacedfootwear (chain),(Whitedoves:1.1)"+
                              "仿照例子，给出一套详细描述以下内容的prompt。直接开始给出prompt，不需要用自然语言描述，只要英文不用解释。尽可能多的单词描述画面和细节，注意每个单词的权重不要超过1.1。"},
                  {"role": "user", "content": f"画面内容：{access}。"}]
    )
    response = completion.choices[0].message.content
    # print(response)
    img_yun_API.text2img(response, emoji)

# if __name__ == '__main__':
    # get_img_memory('一起在散步吧')





