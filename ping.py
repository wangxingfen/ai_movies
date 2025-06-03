import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def add_subtitle_to_video(input_path, output_path, text, font_path='simhei.ttf', font_size=40):
    """
    Add Chinese subtitles to the bottom of a video
    Args:
        input_path: path to input video
        output_path: path to save output video
        text: Chinese text to add as subtitle
        font_path: path to Chinese font file (default simhei.ttf)
        font_size: size of font (default 40)
    """
    # Open video
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Load Chinese font
    font = ImageFont.truetype(font_path, font_size)
    
    # Split text into lines with max 10 characters per line
    lines = [text[i:i+10] for i in range(0, len(text), 10)]
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert frame to PIL Image
        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(frame_pil)
        
        # Calculate text position (centered at bottom)
        total_height = 0
        for line in lines:
            left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
            text_width = right - left
            text_height = bottom - top
            total_height += text_height
        
        x = (width - text_width) // 2
        y = height - total_height - 20  # 20 pixels from bottom
        
        # Draw each line of text
        current_y = y
        for line in lines:
            left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
            text_height = bottom - top
            draw.text((x, current_y), line, font=font, fill=(255, 255, 255))
            current_y += text_height
        
        # Convert back to OpenCV format
        frame_with_text = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        
        # Write frame
        out.write(frame_with_text)
    
    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    return output_path

def add_subtitle_to_image(input_path, output_path, text, font_path='simhei.ttf', font_size=60, color=(255, 255, 255), bold=True):
    """
    Add Chinese subtitles to the center of an image
    Args:
        input_path: path to input image
        output_path: path to save output image
        text: Chinese text to add as subtitle
        font_path: path to Chinese font file (default simhei.ttf)
        font_size: size of font (default 40)
        color: RGB tuple for text color (default white)
        bold: whether to make text bold (default False)
    """
    # Open image using OpenCV
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Could not read image from path: " + input_path)
    
    # Convert to PIL Image
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    # Load Chinese font
    font = ImageFont.truetype(font_path, font_size)
    
    # Split text into lines with max 10 characters per line
    lines = [text[i:i+10] for i in range(0, len(text), 10)]
    
    # Calculate text position (centered)
    total_height = 0
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_width = right - left
        text_height = bottom - top
        total_height += text_height
    
    x = (img.shape[1] - text_width) // 2
    y = (img.shape[0] - total_height) // 2  # Centered vertically
    
    # Draw each line of text
    current_y = y
    for line in lines:
        left, top, right, bottom = draw.textbbox((0, 0), line, font=font)
        text_height = bottom - top
        
        # Draw text with optional bold effect
        if bold:
            # Draw thicker stroke by drawing multiple offset texts
            for adj in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
                draw.text((x+adj[0], current_y+adj[1]), line, font=font, fill=color)
        draw.text((x, current_y), line, font=font, fill=color)
        
        current_y += text_height
    
    # Convert back to OpenCV format and save
    img_with_text = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, img_with_text)
    return output_path

# Example usage:
if __name__ == '__main__':
    #add_subtitle_to_video('temp/1.mp4', 'output.mp4', '这是字幕文字')
    add_subtitle_to_image('images/1.png', 'output.png', '这是图片字幕')