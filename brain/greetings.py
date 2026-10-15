# brain/greetings.py
import random

def handle_greetings(text):
    """
    Offline Greetings Handler: Hi, Hello, Good Morning ka jawab dene ke liye.
    """
    text = text.lower()
    
    hellos = ["hi", "hello", "hey", "hola", "pihu", "online"]
    good_morning = ["good morning", "gm", "suprabhat"]
    good_night = ["good night", "gn", "shubh ratri"]

    if any(word in text for word in hellos):
        return random.choice([
            "Hello Hemant! Kaise ho aap? 😊",
            "Hey Hemant! Pihu is here. Batao aaj kya baatein karni hain?",
            "Hi buddy! Aapki Pihu haazir hai."
        ])
        
    elif any(word in text for word in good_morning):
        return "Good morning Hemant! Aaj ka din aapka bohot accha jaye. ✨"
        
    elif any(word in text for word in good_night):
        return "Good night Hemant! So jao ab, sweet dreams. 😴"
        
    return None