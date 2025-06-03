import requests
import random
from openai import OpenAI
import json
import time
import os
from retrying import retry
@retry(stop_max_attempt_number=200, wait_exponential_multiplier=200, wait_exponential_max=400)
def image_prompt(prompt,config,style_prompt,background,character_prompt):
    '''生成图像提示词'''
    image_prompts=config["image_prompt"]
    client = OpenAI(
    # 请用知识引擎原子能力API Key将下行替换为：api_key="sk-xxx",
    api_key=config["api_key"], # 如何获取API Key：https://cloud.tencent.com/document/product/1772/115970
    base_url=config["base_url"],
)
    completion = client.chat.completions.create(
        model=config['model'],  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        temperature=0,
        messages=[
            {'role': 'system', 'content':f"{image_prompts}请不要遗漏对用户要求中可能存在的角色的描述。\n输出请尽量参考以下画风:\n{style_prompt}\n适度参考以下故事情节，以确保前后场景的连贯性：\n{background}\n描绘用户要求场景的角色时参考以下的描述：\n{character_prompt}\n"},
            {'role': 'user', 'content': prompt}
            ]
)
    img_prompt=completion.choices[0].message.content
    return img_prompt
@retry(stop_max_attempt_number=200, wait_exponential_multiplier=200, wait_exponential_max=400)
def get_image(prompt,i,style_prompt,background,seed=1,character_prompt=None):
    '''生成图像'''
    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        url = config.get('images_base_url')+'/images/generations'
        model = config.get('images_model')
        api_key = config.get('images_api_key')

        if not url or not model or not api_key:
            raise ValueError("图像生成配置不完整，请在设置中配置图像模型相关参数")

        payload = {
            "model": model,
            "prompt": image_prompt(prompt,config,style_prompt,background,character_prompt),
            "seed":seed,
            "image_size": "1152x2048",
            "num_inference_steps": 45,
            "negative_prompt": "bad anime, bad illustration, lowres, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name",
        }
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()
        image_url = response.json()["images"][0]["url"]   
        image_response = requests.get(image_url, timeout=30)
        image_response.raise_for_status()
        file_path = os.path.abspath(os.path.join("images/", str(i) + ".png"))
        print(file_path)

        with open(file_path, 'wb') as f:
            f.write(image_response.content)
        return file_path
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        raise
if __name__ == '__main__':
    print(get_image("一只猪",1))