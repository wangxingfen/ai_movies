import requests
def voice2text(file_path):
    url = "https://api.siliconflow.cn/v1/audio/transcriptions"

    headers = {
        "Authorization": "Bearer sk-aardxirtqpsnhqvocoqblbiirgtoeqmlgldlrzrjondasxll"
    }

    files = {
        'model': (None, 'FunAudioLLM/SenseVoiceSmall'),
        'file': ('output.wav', open(file_path, 'rb'), 'audio/wav')
    }
    response = requests.post(url, headers=headers, files=files)
    print(response.json()["text"])
    return response.json()["text"]
if __name__ == "__main__":
    voice2text("output.wav")