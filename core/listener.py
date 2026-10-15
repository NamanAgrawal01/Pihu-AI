import speech_recognition as sr
import time
import core.voice

def listen():
    if getattr(core.voice, 'is_speaking', False):
        time.sleep(0.3)
        return ""

    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    r.energy_threshold = 300       # बैकग्राउंड आवाज़ को फ़िल्टर करेगा
    r.pause_threshold = 1.0        # बोलने के बीच सांस लेने का समय
    r.non_speaking_duration = 0.4
    
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.4)
        try:
            print("\n🎤 Listening...")
            audio = r.listen(source, phrase_time_limit=12)
            
            if getattr(core.voice, 'is_speaking', False):
                return ""
                
            query = r.recognize_google(audio, language="en-IN")
            print(f"👤 You said: '{query}'")  # यहाँ दिखेगा कि क्या सुना गया
            return query.lower().strip()
        except sr.UnknownValueError:
            return ""
        except Exception:
            return ""

def wait_for_wake_word():
    r = sr.Recognizer()
    r.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.3)
        while True:
            if getattr(core.voice, 'is_speaking', False):
                time.sleep(0.3)
                continue
            try:
                audio = r.listen(source, phrase_time_limit=3)
                wake = r.recognize_google(audio, language="en-IN").lower()
                if any(w in wake for w in ["pihu", "hey pihu"]):
                    return True
            except Exception:
                pass