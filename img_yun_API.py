#coding=utf-8
import requests
import json
from generate_signature import generate_signature
import hashlib
import time
import shutil
import datetime
import io
import base64
import wxchat
from PIL import Image

# ======================================
url_pre = "you_tusiart.com_endpoint"
url = "/v1/jobs"
app_id = "you_tusiart.com_App_id"
private_key_path = "you_private_key.pem"
# ======================================


# 文生图
def text2img(prompt_res, prompt_emoji):
    prompt0 = "LiangBing,big breasts,(deep cleavage:1.1),"
    prompt1 = prompt_res
    prompt = prompt0 + prompt1
    negative_prompt = "EasyNegative"
    data = {
        "request_id": hashlib.md5(str(int(time.time())).encode()).hexdigest(),
        "stages": [
            {
                "type": "INPUT_INITIALIZE",
                "inputInitialize": {
                    "seed": -1,
                    "count": 1
                }
            },
            {
                "type": "DIFFUSION",
                "diffusion": {
                    "width": 512,
                    "height": 768,
                    "prompts": [
                        {
                            "text": prompt
                        }
                    ],
                    "negativePrompts": [
                        {
                        "text": negative_prompt
                        }
                    ],
                    "steps": 20,
                    "sd_model": "666770574388992858",  # checkpoint
                    "sdVae": "Automatic",
                    "sampler": "Euler a",
                    "clip_skip": 2,
                    "cfg_scale": 7,
                    "lora": {
                        "items": [
                            {
                                "loraModel": "678312951104544679",
                                "weight": 0.7
                            },
                            {
                                "loraModel": "617338842296547554",
                                "weight": 0.7
                            },
                            {
                                "loraModel": "681058405869420138",
                                "weight": 0.7
                            }
                        ]
                    }
                }
            },
            {
                "type": "IMAGE_TO_ADETAILER",
                "image_to_adetailer": {
                    "args": [
                        {
                            "ad_model": "face_yolov8n_v2.pt",
                            "ad_confidence": 0.5,
                            "ad_dilate_erode": 4,
                            "ad_denoising_strength": 0.25,
                            "ad_inpaint_only_masked": True,
                            "ad_inpaint_only_masked_padding": 32,
                            "ad_steps": 20,
                            "lora": {
                                "items": [
                                     {
                                     "loraModel": "678312951104544679",
                                     "weight": 1.0
                                     }
                                ]
                            },
                            "ad_prompt": [
                                {
                                    "text": "LiangBing,"+prompt_emoji
                                }
                            ],
                            "ad_negative_prompt": [
                                {
                                    "text": negative_prompt
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
    response_data = create_job(data)
    if 'job' in response_data:
        job_dict = response_data['job']
        job_id = job_dict.get('id')
        job_status = job_dict.get('status')
        # print(job_id, job_status)
        get_job_result(job_id)


def get_job_result(job_id):
    while True:
        time.sleep(1)
        response = requests.get(f"{url_pre}{url}/{job_id}", headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': generate_signature("GET", f"{url}/{job_id}", "", app_id, private_key_path)
        })
        get_job_response_data = json.loads(response.text)
        if 'job' in get_job_response_data:
            job_dict = get_job_response_data['job']
            job_status = job_dict.get('status')
            if job_status == 'SUCCESS':
                img_save(job_dict['successInfo']['images'][0]['url'])
                print(datetime.datetime.now(), job_dict['status'])
                break
            elif job_status == 'FAILED':
                print(job_dict)
                break
            else:
                pass
                # print(job_dict)


def create_job(data):
    body = json.dumps(data)
    auth_header = generate_signature("POST", url, body, app_id, private_key_path)
    response = requests.post(f"{url_pre}{url}", json=data, headers={
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': auth_header
    })
    print(response.text)
    return json.loads(response.text)

def img_save(url_img):
    response = requests.get(url_img)
    image_data = base64.b64encode(response.content)
    image_bytes = base64.b64decode(image_data)
    wxchat.givechat_img(image_bytes)
    image = Image.open(io.BytesIO(image_bytes))
    current_datetime = datetime.datetime.now()  # 获取当前日期时间
    formatted_datetime = current_datetime.strftime("%Y-%m-%d %H-%M-%S").replace(":", "_")  # 格式化日期时间字符串并替换冒号为下划线
    image.save(rf'output\{formatted_datetime}.png')




#if __name__ == '__main__':
    # 文生图
    #text2img("(beautifulgirl:1),(blacklingerie:1),(lyingonbed:1),(sensual:1),(longhair:1),(dark:0.9)", "seductive_smile")