import cv2
import numpy as np
from PIL import Image
from tqdm import tqdm

def create_zoom_video(
    input_path: str,
    output_path: str = "zoom_output.mp4",
    max_zoom: float = 2.0,
    duration: float = 5.0,
    fps: int = 24
):
    """
    Create zoom-out video from an image (from max_zoom back to original size)
    Args:
        input_path: Path to input image
        output_path: Output video path (default: zoom_output.mp4)
        max_zoom: Maximum zoom multiplier at start (default: 2.0)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 30)
    """
    # Read original image
    img = Image.open(input_path)
    orig_width, orig_height = img.size
    
    # Calculate total frames
    total_frames = int(duration * fps)
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (orig_width, orig_height))
    
    # Generate zoom frames
    for frame in tqdm(range(total_frames)):
        # Calculate current zoom factor (linear interpolation from max_zoom to 1)
        zoom = max_zoom - (max_zoom - 1) * (frame / total_frames)
        
        # Calculate new dimensions
        new_width = int(orig_width * zoom)
        new_height = int(orig_height * zoom)
        
        # Resize image with anti-aliasing
        zoomed_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Crop center to original size
        left = (new_width - orig_width) // 2
        top = (new_height - orig_height) // 2
        cropped = zoomed_img.crop((left, top, left+orig_width, top+orig_height))
        
        # Convert to OpenCV format and write frame
        video.write(cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

def create_pan_video(
    input_path: str,
    output_path: str = "pan_output.mp4",
    direction: str = "right",
    duration: float = 5.0,
    fps: int = 60
):
    """
    Create panning video from an image that loops continuously
    Args:
        input_path: Path to input image
        output_path: Output video path (default: pan_output.mp4)
        direction: Pan direction (left/right/up/down, default: right)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 60)
    """
    img = Image.open(input_path)
    width, height = img.size
    
    # Create a larger canvas to allow seamless panning
    if direction in ["left", "right"]:
        extended_img = Image.new('RGB', (width * 2, height))
        extended_img.paste(img, (0, 0))
        extended_img.paste(img, (width, 0))
    else:  # up/down
        extended_img = Image.new('RGB', (width, height * 2))
        extended_img.paste(img, (0, 0))
        extended_img.paste(img, (0, height))
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in tqdm(range(total_frames)):
        progress = frame / total_frames
        if direction == "right":
            x_offset = int(width * progress)
            cropped = extended_img.crop((x_offset, 0, x_offset + width, height))
        elif direction == "left":
            x_offset = int(width * (1 - progress))
            cropped = extended_img.crop((x_offset, 0, x_offset + width, height))
        elif direction == "down":
            y_offset = int(height * progress)
            cropped = extended_img.crop((0, y_offset, width, y_offset + height))
        elif direction == "up":
            y_offset = int(height * (1 - progress))
            cropped = extended_img.crop((0, y_offset, width, y_offset + height))
            
        video.write(cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

def create_rotation_video(
    input_path: str,
    output_path: str = "rotate_output.mp4",
    rotation_degrees: float = 90,
    duration: float = 5.0,
    fps: int = 60,
    max_scale: float = 2.0
):
    """
    Create rotating video from an image with zoom-in effect that alternates between left and right rotation
    Args:
        input_path: Path to input image
        output_path: Output video path (default: rotate_output.mp4)
        rotation_degrees: Total rotation degrees in each direction (default: 90)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 60)
        max_scale: Maximum scale factor during rotation (default: 2.0)
    """
    img = Image.open(input_path)
    width, height = img.size
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in tqdm(range(total_frames)):
        progress = frame / total_frames
        # Use sine wave to create alternating rotation pattern
        angle = rotation_degrees * np.sin(2 * np.pi * progress)
        scale = 1 + (max_scale - 1) * abs(np.sin(np.pi * progress))  # Scale peaks at each turn
        
        # Rotate and scale the image
        rotated = img.rotate(angle, expand=True)
        
        # Apply scaling
        scaled_width = int(rotated.width * scale)
        scaled_height = int(rotated.height * scale)
        scaled = rotated.resize((scaled_width, scaled_height), Image.LANCZOS)
        
        # Center the rotated and scaled image
        bg = Image.new('RGB', (width, height))
        bg.paste(scaled, ((width - scaled.width) // 2, (height - scaled.height) // 2))
        
        video.write(cv2.cvtColor(np.array(bg), cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

def create_shake_zoom_video(
    input_path: str,
    output_path: str = "shake_zoom_output.mp4",
    max_zoom: float = 2.0,
    duration: float = 5.0,
    fps: int = 24,
    shake_intensity: float = 0.1
):
    """
    Create zoom-out video with shaking effect
    Args:
        input_path: Path to input image
        output_path: Output video path (default: shake_zoom_output.mp4)
        max_zoom: Maximum zoom multiplier at start (default: 2.0)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 30)
        shake_intensity: Intensity of the shaking effect (default: 0.1)
    """
    img = Image.open(input_path)
    orig_width, orig_height = img.size
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (orig_width, orig_height))
    
    for frame in tqdm(range(total_frames)):
        # Calculate current zoom factor
        zoom = max_zoom - (max_zoom - 1) * (frame / total_frames)
        
        # Calculate random offset for shaking effect
        x_offset = int(orig_width * shake_intensity * (np.random.random() - 0.5))
        y_offset = int(orig_height * shake_intensity * (np.random.random() - 0.5))
        
        new_width = int(orig_width * zoom)
        new_height = int(orig_height * zoom)
        zoomed_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Apply shaking offset to crop position
        left = (new_width - orig_width) // 2 + x_offset
        top = (new_height - orig_height) // 2 + y_offset
        cropped = zoomed_img.crop((left, top, left+orig_width, top+orig_height))
        
        video.write(cv2.cvtColor(np.array(cropped), cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

def create_color_shift_video(
    input_path: str,
    output_path: str = "color_shift_output.mp4",
    duration: float = 5.0,
    fps: int = 60,
    color_shift_speed: float = 2.0
):
    """
    Create video with continuously shifting colors
    Args:
        input_path: Path to input image
        output_path: Output video path (default: color_shift_output.mp4)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 60)
        color_shift_speed: Speed of color shifting (default: 2.0)
    """
    img = Image.open(input_path)
    width, height = img.size
    img_array = np.array(img)
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in tqdm(range(total_frames)):
        progress = frame / total_frames
        # Calculate color shift values (sine waves for smooth transitions)
        r_shift = np.sin(progress * color_shift_speed * 2 * np.pi) * 50
        g_shift = np.sin(progress * color_shift_speed * 2 * np.pi + 2*np.pi/3) * 50
        b_shift = np.sin(progress * color_shift_speed * 2 * np.pi + 4*np.pi/3) * 50
        
        # Apply color shift
        shifted = img_array.astype(np.float32)
        shifted[..., 0] = np.clip(shifted[..., 0] + r_shift, 0, 255)
        shifted[..., 1] = np.clip(shifted[..., 1] + g_shift, 0, 255)
        shifted[..., 2] = np.clip(shifted[..., 2] + b_shift, 0, 255)
        
        video.write(shifted.astype(np.uint8))
    
    video.release()
    return output_path

def create_ripple_video(
    input_path: str,
    output_path: str = "ripple_output.mp4",
    duration: float = 5.0,
    fps: int = 60,
    ripple_frequency: float = 0.4,
    ripple_amplitude: float = 10
):
    """
    Create ripple distortion effect video from an image
    Args:
        input_path: Path to input image
        output_path: Output video path (default: ripple_output.mp4)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 60)
        ripple_frequency: Controls how tight the ripples are (default: 0.1)
        ripple_amplitude: Controls how strong the distortion is (default: 50)
    """
    img = Image.open(input_path)
    width, height = img.size
    img_array = np.array(img)
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    x = np.arange(width)
    y = np.arange(height)
    xx, yy = np.meshgrid(x, y)
    
    for frame in tqdm(range(total_frames)):
        progress = frame / total_frames
        # Calculate current amplitude (fading from full to zero)
        current_amplitude = ripple_amplitude * (1 - progress)
        
        # Create dynamic ripple effect with fading amplitude
        ripple = current_amplitude * np.sin(ripple_frequency * np.sqrt((xx - width/2)**2 + (yy - height/2)**2) - 10 * progress * np.pi)
        
        # Apply ripple distortion
        xmap = xx + ripple * np.cos(progress * np.pi)
        ymap = yy + ripple * np.sin(progress * np.pi)
        
        # Normalize and remap
        xmap = np.clip(xmap, 0, width-1).astype(np.float32)
        ymap = np.clip(ymap, 0, height-1).astype(np.float32)
        
        distorted = cv2.remap(img_array, xmap, ymap, cv2.INTER_LINEAR)
        video.write(cv2.cvtColor(distorted, cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

def create_splitslide_video(
    input_path: str,
    output_path: str = "splitslide_output.mp4",
    duration: float = 5.0,
    fps: int = 30,
    split_direction: str = "vertical",
    num_splits: int = 4
):
    """
    Create video where image splits into pieces and slides back together
    Args:
        input_path: Path to input image
        output_path: Output video path (default: splitslide_output.mp4)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 30)
        split_direction: Direction of splits (vertical/horizontal, default: vertical)
        num_splits: Number of splits (default: 4)
    """
    img = Image.open(input_path)
    width, height = img.size
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in tqdm(range(total_frames)):
        progress = frame / total_frames
        
        if split_direction == "vertical":
            split_size = width // num_splits
            split_images = []
            for i in range(num_splits):
                # Split image into vertical strips
                left = i * split_size
                right = left + split_size if i < num_splits-1 else width
                strip = img.crop((left, 0, right, height))
                
                # Apply sliding animation
                offset = int((1 - abs(2*progress - 1)) * height * 0.5 * (1 if i%2 else -1))
                strip = strip.transform((strip.width, height), Image.AFFINE, 
                                      (1, 0, 0, 0, 1, offset), Image.BICUBIC)
                split_images.append(strip)
            
            # Combine strips back together
            combined = Image.new('RGB', (width, height))
            for i, strip in enumerate(split_images):
                left = i * split_size
                combined.paste(strip, (left, 0))
        
        else:  # horizontal
            split_size = height // num_splits
            split_images = []
            for i in range(num_splits):
                # Split image into horizontal strips
                top = i * split_size
                bottom = top + split_size if i < num_splits-1 else height
                strip = img.crop((0, top, width, bottom))
                
                # Apply sliding animation
                offset = int((1 - abs(2*progress - 1)) * width * 0.5 * (1 if i%2 else -1))
                strip = strip.transform((width, strip.height), Image.AFFINE, 
                                      (1, 0, offset, 0, 1, 0), Image.BICUBIC)
                split_images.append(strip)
            
            # Combine strips back together
            combined = Image.new('RGB', (width, height))
            for i, strip in enumerate(split_images):
                top = i * split_size
                combined.paste(strip, (0, top))
        
        video.write(cv2.cvtColor(np.array(combined), cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

def create_puzzle_reveal_video(
    input_path: str,
    output_path: str = "puzzle_output.mp4",
    duration: float = 5.0,
    fps: int = 30,
    puzzle_size: int = 16
):
    """
    Create puzzle reveal effect where image splits into puzzle pieces that come together
    Args:
        input_path: Path to input image
        output_path: Output video path (default: puzzle_output.mp4)
        duration: Video duration in seconds (default: 5)
        fps: Frames per second (default: 30)
        puzzle_size: Number of pieces per side (default: 4)
    """
    img = Image.open(input_path)
    width, height = img.size
    
    total_frames = int(duration * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    piece_width = width // puzzle_size
    piece_height = height // puzzle_size
    
    for frame in tqdm(range(total_frames)):
        progress = frame / total_frames
        
        result = Image.new('RGB', (width, height))
        for y in range(puzzle_size):
            for x in range(puzzle_size):
                # Calculate piece position
                left = x * piece_width
                upper = y * piece_height
                right = left + piece_width if x < puzzle_size-1 else width
                lower = upper + piece_height if y < puzzle_size-1 else height
                
                # Get original piece
                piece = img.crop((left, upper, right, lower))
                
                # Apply animation - pieces come from random directions
                if progress < 0.8:
                    # Reduced amplitude by changing multiplier from 0.5 to 0.3
                    offset_x = int((width * 0.1) * (1 - progress/0.8) * (np.random.random() - 0.5))
                    offset_y = int((height * 0.1) * (1 - progress/0.8) * (np.random.random() - 0.5))
                    result.paste(piece, (left + offset_x, upper + offset_y))
                else:
                    result.paste(piece, (left, upper))
        
        video.write(cv2.cvtColor(np.array(result), cv2.COLOR_RGB2BGR))
    
    video.release()
    return output_path

if __name__ == '__main__':
    create_ripple_video(input_path="images/1.png")