import json
import os

MEMORY_FILE = "pihu_memory.json"

def save_memory(user, pihu):
    # Purana data load karo
    data = load_memory()
    # Naya record add karo
    data.append({"u": user, "p": pihu})
    # Sirf last 5 baatein rakho taaki Pihu confuse na ho
    with open(MEMORY_FILE, "w") as f: 
        json.dump(data[-5:], f) 

def load_memory():
    if not os.path.exists(MEMORY_FILE): 
        return []
    with open(MEMORY_FILE, "r") as f: 
        try:
            return json.load(f)
        except:
            return []