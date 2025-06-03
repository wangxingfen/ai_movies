import os
from moviepy import VideoFileClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip

def add_subtitles(video_path, output_path, subtitles, 
                 font='Arial', fontsize=24, color='white',
                 bg_color=None, stroke_color=None, stroke_width=1,
                 position=('center', 'bottom')):
    """
    Add subtitles to a video
    :param video_path: path to input video
    :param output_path: path to save output video
    :param subtitles: list of tuples (start_time, end_time, text)
    :param font: font name
    :param fontsize: font size
    :param color: text color
    :param bg_color: background color (optional)
    :param stroke_color: text stroke color (optional)
    :param stroke_width: text stroke width
    :param position: tuple (x, y) position of subtitles
    """
    video = VideoFileClip(video_path)
    
    # Create subtitle clips
    subtitle_clips = []
    for start, end, text in subtitles:
        txt_clip = TextClip(text, font=font, fontsize=fontsize, color=color,
                           stroke_color=stroke_color, stroke_width=stroke_width,
                           bg_color=bg_color)
        txt_clip = txt_clip.set_position(position).set_duration(end-start).set_start(start)
        subtitle_clips.append(txt_clip)
    
    # Combine video and subtitles
    final_video = CompositeVideoClip([video] + subtitle_clips)
    
    # Write output
    final_video.write_videofile(output_path, codec="h264_nvenc", audio_codec="aac")
    final_video.close()
    video.close()

def conbine_videos(folder_path):
    # 获取文件夹中所有视频文件
    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if not video_files:
        print("文件夹中没有视频文件")
        return None
    
    # 按文件名数字顺序排序
    video_files = sorted(video_files, key=lambda x: int(x.split('.')[0]))
    
    # 加载视频文件
    clips = []
    for video_file in video_files:
        clip = VideoFileClip(os.path.join(folder_path, video_file))
        clips.append(clip)
    print("开始拼接视频")

    # 拼接视频（按顺序合并）
    final_clip = concatenate_videoclips(clips, method="compose")

    # 输出合并后的视频，启用CUDA加速
    final_clip.write_videofile(
        "output.mp4", 
        codec="h264_nvenc",  # 使用CUDA加速的H.264编码器
        audio_codec="aac"
    )
    #绝对路径
    output_path=os.path.abspath("output.mp4")
    # 关闭合并视频操作以实现安全退出
    final_clip.close()
    for clip in clips:
        clip.close()
        return output_path
def clear_folder(folder_path):
    # 删除文件夹内的所有内容
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"已删除文件: {file_name}")
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
                print(f"已删除文件夹: {file_name}")
        except Exception as e:
            print(f"无法删除 {file_name}: {e}")
    print(print(f"{folder_path}文件夹内内容已清空"))
    