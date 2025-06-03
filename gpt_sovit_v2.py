import wave
import contextlib
import re
import json
import requests
import os
current_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 使用 POST 方法调用 TTS 接口的函数
def post_tts(data):
    url = "http://127.0.0.1:9880/tts"
    headers = {
        'Connection': 'close'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.content  # 返回音频流
    else:
        return response.json()  # 返回错误信息

# 控制服务器的函数
def control_server(command):
    url = "http://127.0.0.1:9880/control"
    params = {"command": command}
    response = requests.get(url, params=params)
    return response.status_code

# 设置 GPT 权重的函数
def set_gpt_weights(weights_path):
    url = "http://127.0.0.1:9880/set_gpt_weights"
    params = {"weights_path": weights_path}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return "success"
    else:
        return response.json()  # 返回错误信息

# 设置 Sovits 权重的函数
def set_sovits_weights(weights_path):
    url = "http://127.0.0.1:9880/set_sovits_weights"
    params = {"weights_path": weights_path}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return "success"
    else:
        return response.json()  # 返回错误信息
    



class gpt_sovits:
    def calculate_audio_duration(self,audio_path):
        with contextlib.closing(wave.open(audio_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            return frames / float(rate)

    def time(self, text,character_name,is_enable=True):
        with open("gpt_sovits.json", "r", encoding="utf-8") as f:
            gpt_config = json.load(f)
            character=gpt_config[character_name]
        #ref_audio_path,prompt_text,GPT_weights_path,Sovits_weights_path
        text_lang="zh"
        prompt_lang="zh"
        text_split_method="cut5"
        batch_size=1
        media_type="wav"
        GPT_weights_path=character["GPT_weights_path"]
        Sovits_weights_path=character["Sovits_weights_path"]
        if is_enable == False:
            return (None,)
        if GPT_weights_path != "":
            set_gpt_weights(GPT_weights_path)
        if Sovits_weights_path != "":
            set_sovits_weights(Sovits_weights_path)
        # 如果text_lang=zh,删除text中所有的非中文字符（包含英文标点，不包含中文标点）
        if text_lang == "zh":
            text = re.sub(r'[^\u4e00-\u9fa5，。！？；：、（）《》“”‘’]', '', text)
        data = {
    "text": text,
    "text_lang": text_lang,
    "ref_audio_path": character["ref_audio_path"],
    "prompt_text": character["prompt_text"],
    "prompt_lang": prompt_lang,
    "text_split_method": text_split_method,
    "batch_size": batch_size,
    "media_type": media_type,
    "streaming_mode": False,
}
        audio_stream = post_tts(data)
        # 如果audio_stream是一个字典
        if isinstance(audio_stream, dict):
            print("audio_stream is a dict:", audio_stream)
        # 判断当前目录是否存在audio文件夹，如果不存在则创建
        if not os.path.exists(os.path.join(current_dir_path, "audio")):
            os.makedirs(os.path.join(current_dir_path, "audio"))
        #timestamp = int(time.time() * 1000)
        full_audio_path = os.path.join(current_dir_path, "audio", f"1.{media_type}")
        with open(full_audio_path, "wb") as f:
            f.write(audio_stream)
        out = full_audio_path
        audio_path = out
        #waveform, sample_rate = torchaudio.load(audio_path)
        #audio_out = {"waveform": waveform.unsqueeze(0), "sample_rate": sample_rate}
        return audio_path
def save():
    with  open("tools/gpt_sovits.json", "r",encoding='utf-8') as f:
        gpt_config = json.load(f)
    gpt_config["莱卡恩"]={
        "ref_audio_path":"D:/AI/GPT-SoVITS-v3lora-20250228/refer_audio/莱卡恩/不过如果真如阁下所说，这位发帖人只是在恶作剧的话，倒也无妨。.wav",
        "prompt_text":"不过如果真如阁下所说，这位发帖人只是在恶作剧的话，倒也无妨。",
        "GPT_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\莱卡恩-e10.ckpt",
        "Sovits_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\莱卡恩_e10_s560.pth",

        }
    with  open("tools/gpt_sovits.json", "w",encoding='utf-8') as f:
        json.dump(gpt_config, f, indent=4,ensure_ascii=False)
def save1():
    with  open("tools/gpt_sovits.json", "r",encoding='utf-8') as f:
        gpt_config = json.load(f)
    gpt_config["星见雅"]={
        "ref_audio_path":"D:/AI/GPT-SoVITS-v3lora-20250228/refer_audio/雅/难过_sad/【难过_sad】就像你追求真正的正义一样，蜜瓜就是蜜瓜绝不会变成假的。.wav",
        "prompt_text":"就像你追求真正的正义一样，蜜瓜就是蜜瓜绝不会变成假的。",
        "GPT_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\雅-e10.ckpt",
        "Sovits_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\雅_e10_s170.pth",

        }
    with  open("tools/gpt_sovits.json", "w",encoding='utf-8') as f:
        json.dump(gpt_config, f, indent=4,ensure_ascii=False)
def save2():
    with  open("tools/gpt_sovits.json", "r",encoding='utf-8') as f:
        gpt_config = json.load(f)
    gpt_config["苍角"]={
        "ref_audio_path":"D:/AI/GPT-SoVITS-v3lora-20250228/refer_audio/苍角/另外关于吃的我完全没有忌口，只要是好吃的，我什么都可以吃啊。.wav",
        "prompt_text":"另外关于吃的我完全没有忌口，只要是好吃的，我什么都可以吃啊。",
        "GPT_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\苍角-e10.ckpt",
        "Sovits_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\苍角_e10_s110.pth",

        }
    with  open("tools/gpt_sovits.json", "w",encoding='utf-8') as f:
        json.dump(gpt_config, f, indent=4,ensure_ascii=False)
def save3():
    with  open("tools/gpt_sovits.json", "r",encoding='utf-8') as f:
        gpt_config = json.load(f)
    gpt_config["光头强"]={
        "ref_audio_path":"D:/AI/GPT-SoVITS-v3lora-20250228/refer_audio/光头强/没人哪，难道我听错了？算了，吃饱了睡会儿去，晚上还得干活.wav",
        "prompt_text":"没人哪，难道我听错了？算了，吃饱了睡会儿去，晚上还得干活。",
        "GPT_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\GPT_weights_v3\\guangtouqiang-e15.ckpt",
        "Sovits_weights_path":"D:\\AI\\GPT-SoVITS-v3lora-20250228\\SoVITS_weights_v3\\guangtouqiang_e4_s100.pth",

        }
    with  open("tools/gpt_sovits.json", "w",encoding='utf-8') as f:
        json.dump(gpt_config, f, indent=4,ensure_ascii=False)
if __name__ == "__main__":
    save3()
    gpt_sovits().time("我是光头强啊，你怎么称呼？","光头强")
        