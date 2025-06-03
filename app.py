from movies_images import get_image
from blender import mix_audio_into_video
from video_prompt import video_prompt,video_style,video_characters
from movie_made import conbine_videos,clear_folder
import os
import asyncio
from zoom import *
import concurrent.futures
import re
from gpt_sovit_v2  import gpt_sovits
import random
import contextlib
from pydub import AudioSegment
import wave
import edge_tts
import json
from ping import add_subtitle_to_image
def excute_functions(name,input_path,duration,output_path,fps):
    try:
        function_object = globals()[name]  # 使用 globals() 获取全局命名空间中的函数    
        function_result = function_object(input_path=input_path,duration=duration,output_path=output_path,fps=fps)
        return function_result
    except Exception as e:
        return f"Error: {str(e)}"
async def text_to_speech_edge(
    text: str,
    voice: str = "zh-CN-YunxiNeural",
    rate: str = "+0%",
    volume: str = "+0%",
    filename: str = "output.wav"
) -> str:
    """
    Convert text to speech using Edge TTS (online Microsoft voices)
    
    Args:
        text: Input string to be spoken
        voice: Voice name (default: zh-CN-YunxiNeural)
        rate: Speaking rate adjustment (e.g. "+10%" or "-10%")
        volume: Volume adjustment (e.g. "+10%" or "-10%")
        filename: Optional output path to save as .mp3 file
        
    Returns:
        Path to saved file if filename provided, else None
        
    Raises:
        ValueError: If input text is empty or not a string
        RuntimeError: If TTS fails
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")
    
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
        
        if filename:
            await communicate.save(filename)
            return filename
        else:
            await communicate.stream()
            return None
            
    except Exception as e:
        raise RuntimeError(f"Edge TTS failed: {str(e)}") from e

def calculate_audio_duration(audio_path):
    audio = AudioSegment.from_file(audio_path)
    return len(audio) / 1000.0  # Duration in seconds
def get_functions_from_file(file_path):
    """Get all function names from a Python file.
    
    Args:
        file_path (str): Path to the Python file
        
    Returns:
        list: List of function names in the file
    """
    function_names = []
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            if line.strip().startswith('def '):
                # Extract function name
                function_name = line.split('def ')[1].split('(')[0].strip()
                function_names.append(function_name)
    return function_names

def main(topic):
    if os.path.exists("temp"):
        clear_folder("temp")
    #effects_list = get_functions_from_file("zoom.py")
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("images"):
        os.mkdir("images")
    
    if not os.path.exists("temp"):
        os.mkdir("temp")
    if not os.path.exists("images"):
        os.mkdir("images")
    effects_list = get_functions_from_file("zoom.py")
    base_prompts=video_prompt(topic)
    print(base_prompts)
    style_prompt=video_style(base_prompts)
    print(style_prompt)
    prompts = re.split('，|。|！|？|：',base_prompts)
    #prompts =prompts.split("。")
    seed=random.randint(1, 10000000000)
    character_prompt=video_characters(str(base_prompts))
    print(character_prompt)
    for i in range(len(prompts)):
        try:
            audio_path="output.wav"
            asyncio.run(text_to_speech_edge(text=str(prompts[i]).strip(), filename=audio_path))
            print(prompts[i])
            print(f"进度{i+1}/{len(prompts)}")
            img_path=get_image(str(prompts[i]), 1, style_prompt, str(prompts),seed=seed,character_prompt=character_prompt)
                #audio_future = executor.submit(gpt_sovits().time, prompts[i], "莱卡恩")
                #audio_future = executor.submit(text_to_speech, text=str(prompts[i]),filename="temp.mp3")
                #audio_path = audio_future.result()
            duration = calculate_audio_duration(audio_path)
            random_number = random.randint(0, len(effects_list) - 1)
            random_effect = effects_list[random_number]
            img_path=add_subtitle_to_image(input_path=img_path,output_path=img_path,text=str(prompts[i]).strip())
            effect_output_path = "effect_output.mp4"
            #output_path=create_zoom_video(input_path=img_path, output_path=effect_output_path,duration=duration,fps=24)
            output_path=excute_functions(random_effect,img_path,duration,effect_output_path,fps=24)
            output_path=mix_audio_into_video(output_path, audio_path, f"temp/{i+1}.mp4")
        except Exception as e:
            print(e)
        
    output_path=conbine_videos("temp")
    print(f"视频合成完成！已经保存在: {output_path}")

if __name__ == "__main__":
    if not os.path.exists("settings.json"):
        with open("settings.json", "w",encoding="utf-8") as f:
            config = {
                "base_url": "https://api.siliconflow.cn/v1",
                "model": "THUDM/glm-4-9b-chat",
                "images_base_url": "https://api.siliconflow.cn/v1",
                "images_model": "black-forest-labs/FLUX.1-schnell",
                "image_prompt": "请将用户的输入升华具有大师水准的准确且标准且丰富的的英文绘图提示词，请尽可能让画面栩栩如生，以便绘图模型能够完美绘制。"
            }

            json.dump(config, f,ensure_ascii=False,indent=4)
    input_path=int(input("你是否已经设置了大模型密钥？1.是 2.否 \n"))
    if input_path==2:
        with  open("settings.json", "r",encoding='utf-8') as f:
            config = json.load(f)
            key=input("如果没有注册密钥请到https://cloud.siliconflow.cn/i/ByXrxmTh，进行注册，然后进入个人主页，然后进入api密钥区域新建密钥，然后请输入硅基流动的API密钥：")
            config['api_key']=key
            config["images_api_key"]=key

        with open("settings.json", "w",encoding='utf-8') as f:
            json.dump(config, f,ensure_ascii=False,indent=4)
    topic= input("请输入主题：")
    main(topic=topic)
    #conbine_videos("temp")