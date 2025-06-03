import os
from moviepy import VideoFileClip, AudioFileClip  # 修改：从moviepy.editor模块导入所需类

def mix_audio_into_video(video_path, audio_path, output_path):
    """
    将.mp3音频混入.mp4视频文件

    参数:
    video_path (str): 输入视频文件的路径
    audio_path (str): 输入音频文件的路径
    output_path (str): 输出视频文件的路径
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件未找到: {video_path}")
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"音频文件未找到: {audio_path}")

        # 加载视频和音频
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # 使用with_audio方法替换视频的音频
        video = video.with_audio(audio)
        
        # 导出新的视频文件
        video.write_videofile(output_path, codec='libx264', audio_codec='aac')
        print(f"视频已成功导出到: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"发生错误: {e}")

# 示例用法
if __name__ == "__main__":
    video_path = "anan.mp4"
    audio_path = "10.mp3"
    output_path = "output_video.mp4"
    
    mix_audio_into_video(video_path, audio_path, output_path)