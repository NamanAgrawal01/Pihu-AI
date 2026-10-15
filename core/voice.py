import asyncio
import edge_tts
import pygame
import os
import uuid
import time
import re
import pyttsx3

try:
    from gui.gui_manager import get_app
except ImportError:
    def get_app():
        return None

is_speaking = False
VOICE = "hi-IN-SwaraNeural"
os.makedirs("temp", exist_ok=True)

# ऑफलाइन बैकअप इंजन
offline_engine = None
try:
    offline_engine = pyttsx3.init()
    offline_engine.setProperty('rate', 190)
    voices = offline_engine.getProperty('voices')
    for v in voices:
        if "female" in v.name.lower() or "zira" in v.name.lower() or "hindi" in v.name.lower():
            offline_engine.setProperty('voice', v.id)
            break
except Exception:
    pass

def ensure_mixer():
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except Exception:
            pass

async def generate(clean_text, filename):
    communicate = edge_tts.Communicate(text=clean_text, voice=VOICE, rate="+8%")
    await communicate.save(filename)

def speak(text):
    global is_speaking
    if not text:
        return
    
    is_speaking = True
    app = get_app()
    filename = os.path.join("temp", f"{uuid.uuid4().hex}.mp3")
    
    try:
        ensure_mixer()
        if app and hasattr(app, 'start_talking'):
            app.start_talking()
        
        clean_text = re.sub(r'[*#_~`>]', '', str(text)).strip()
        print(f"🤖 Pihu: {clean_text}")
        
        # 1. पहले Edge TTS से बोलने की कोशिश
        try:
            asyncio.run(generate(clean_text, filename))
            if pygame.mixer.get_init() and os.path.exists(filename):
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.05)
                pygame.mixer.music.unload()
        except Exception:
            # 2. अगर इंटरनेट ड्रॉप हो तो ऑफलाइन बोलेगी
            if offline_engine:
                offline_engine.say(clean_text)
                offline_engine.runAndWait()
    
    except Exception as e:
        print(f"Voice Error: {e}")
    finally:
        if app and hasattr(app, 'stop_talking'):
            app.stop_talking()
        
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception:
                pass
        
        time.sleep(0.3)
        is_speaking = False