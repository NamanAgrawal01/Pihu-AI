import os
import webbrowser

def handle_command(command):
    c = command.lower()
    
    # YouTube ke liye keywords
    if any(word in c for word in ["youtube", "yutube", "युटुब", "video"]):
        webbrowser.open("https://www.youtube.com")
        return "Theek hai Hemant, YouTube khol rahi hoon."
    
    # Google ke liye keywords
    if any(word in c for word in ["google", "search", "ढूंढो"]):
        webbrowser.open("https://www.google.com")
        return "Google khul gaya!"
        
    return None # Agar command nahi mili, toh AI (conversation) handle karegi