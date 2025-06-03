from openai import OpenAI
import json
from retrying import retry
@retry(stop_max_attempt_number=200, wait_exponential_multiplier=100, wait_exponential_max=100)
def video_prompt(code_prompt):
    '''执行具体写代码任务'''
    with open("settings.json", "r",encoding='utf-8') as f:
        config = json.load(f)
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你是一位伟大的电影编剧，根据用户提示为出发点，请完全使用中文栩栩如生且丰富地描绘一个完整的电影剧情，800字左右，循序渐进，每个场景以句号结束。禁止输出序号，场景几，阿拉伯数字等与内容无关的格式,年代时间等数字形式请以中文描述。请确保故事精彩连贯。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':code_prompt},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages
    )
    
    last_code = completion.choices[0].message.content
    return last_code
@retry(stop_max_attempt_number=200, wait_exponential_multiplier=100, wait_exponential_max=100)
def video_style(code_prompt):
    '''执行具体写代码任务'''
    with open("settings.json", "r",encoding='utf-8') as f:
        config = json.load(f)
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你是一个负责给ai控制绘画风格的专家，请用50个字左右总结以上电影剧本的基本情感基调和绘画风格，以供绘图模型参考。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':code_prompt},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=0
    )
    
    last_code = completion.choices[0].message.content
    return last_code
@retry(stop_max_attempt_number=200, wait_exponential_multiplier=100, wait_exponential_max=100)
def video_characters(code_prompt):
    '''执行具体写代码任务'''
    with open("settings.json", "r",encoding='utf-8') as f:
        config = json.load(f)
    client = OpenAI(
        api_key=config["api_key"],
        base_url=config["base_url"]
    )
    tippieces=f'你负责简要归纳用户提供的剧本里主要角色的外貌形象描述，以供绘图模型参考。每个角色20个字左右即可。'
    messages = [
        {'role': 'system', 'content':tippieces},
        {'role': 'user', 'content':code_prompt},
    ]
    
    completion = client.chat.completions.create(
        model=config['model'],
        messages=messages,
        temperature=0
    )
    
    last_code = completion.choices[0].message.content
    return last_code
if  __name__ == '__main__':
    video_outline=video_prompt('电影 蝙蝠侠')
    video_character=video_characters(video_outline)
    print(video_character)
