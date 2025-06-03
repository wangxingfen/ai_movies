import pyttsx3
import edge_tts
import asyncio

def text_to_speech(
    text: str,
    rate: float = None,
    volume: float = None,
    filename: str = None  # Add filename parameter for output file
) -> None:
    """
    Convert text to speech using system's TTS engine
    
    Args:
        text: Input string to be spoken
        rate: Speech rate in words per minute (default: 200)
        volume: Volume level between 0.0 and 1.0 (default: 1.0)
        filename: Optional output path to save as .wav file
        
    Raises:
        RuntimeError: If TTS engine initialization fails
        ValueError: If input text is empty or not a string
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string")
    
    try:
        engine = pyttsx3.init()
        
        # Set speech properties if provided
        if rate is not None:
            engine.setProperty('rate', rate)
        if volume is not None:
            engine.setProperty('volume', volume)
            
        if filename:
            engine.save_to_file(text, filename)  # Add file save capability
        else:
            engine.say(text)
            
        engine.runAndWait()
        engine.stop()
        return filename
        
    except Exception as e:
        raise RuntimeError(f"TTS engine initialization failed: {str(e)}") from e

async def text_to_speech_edge(
    text: str,
    voice: str = "zh-CN-YunxiNeural",
    rate: str = "+50%",
    volume: str = "+0%",
    filename: str = None
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

if __name__=="__main__":
    text_to_speech_edge("这是一个伟大的时刻", filename="output.wav")  # Update test call with filename
