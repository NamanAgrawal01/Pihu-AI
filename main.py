import sys
import os
import pygame
pygame.mixer.init()
import time
import threading
import json
import customtkinter as ctk
from PIL import Image, ImageTk
import core.voice
from brain.conversation import chat_with_pihu
from core.voice import speak
from core.listener import listen
from brain.offline_brain import engine

# 🌟 ग्लोबल वेरिएबल (सबटाइटल्स के लिए)
CURRENT_USER = "Hemant"
SUB_USER = "..." 
SUB_PIHU = "Welcome Boss!"

# --- 0. PATH FINDER ---
def get_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- 1. USER DATA LOGIC ---
DATA_FILE = get_path('data/pihu_memory.json')

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}}
    try:
        with open(DATA_FILE, 'r', encoding="utf-8") as file:
            return json.load(file)
    except:
        return {"users": {}}

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# --- 2. INTRO & PROFILE SCREEN ---
def show_intro_screen():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Pihu AI - System Launcher")
    try:
        app.iconbitmap(get_path("logo.ico"))
    except:
        pass
    app.geometry("850x600")  
    app.resizable(False, False)

    data = load_data()
    default_name = data.get('last_user', "Hemant")
    if not default_name:
        existing_users = list(data.get('users', {}).keys())
        default_name = existing_users[-1] if existing_users else "Hemant"

    left_frame = ctk.CTkFrame(app, corner_radius=0, fg_color="transparent")
    left_frame.pack(side="left", fill="y", padx=40, pady=40)

    try:
        img_path = get_path("assets/avatar/idle.png")
        avatar_img = ctk.CTkImage(light_image=Image.open(img_path), dark_image=Image.open(img_path), size=(150, 150))
        ctk.CTkLabel(left_frame, image=avatar_img, text="").pack(pady=(10, 10))
    except:
        ctk.CTkLabel(left_frame, text="[Avatar Ready]").pack(pady=(10, 10))

    ctk.CTkLabel(left_frame, text="PIHU AI SYSTEM", font=("Arial", 28, "bold"), text_color="#00FFFF").pack(pady=5)
    ctk.CTkLabel(left_frame, text="Version 3.0 - Groq Cloud Edition", font=("Arial", 12), text_color="gray").pack(pady=(0, 20))

    ctk.CTkLabel(left_frame, text=f"Welcome Back, {default_name}!", font=("Arial", 14), text_color="lightgreen").pack(pady=5)

    name_entry = ctk.CTkEntry(left_frame, placeholder_text="Enter your name...", width=250, height=45, corner_radius=10, font=("Arial", 16))
    name_entry.pack(pady=10)
    name_entry.insert(0, default_name)

    def save_and_start():
        global CURRENT_USER  
        user_name = name_entry.get().strip()
        if not user_name: user_name = "Hemant" 
            
        CURRENT_USER = user_name  
        try: 
            engine.curr_user = user_name
        except: 
            pass
            
        if user_name not in data.get('users', {}):
            if 'users' not in data: data['users'] = {}
            data['users'][user_name] = {"context": ""}
            
        data['last_user'] = user_name 
        save_data(data)
        app.destroy()

    start_btn = ctk.CTkButton(left_frame, text="🚀 START PIHU AI", command=save_and_start, width=250, height=50,
                              corner_radius=25, fg_color="#00FFFF", text_color="black", hover_color="#00CCCC", font=("Arial", 16, "bold"))
    start_btn.pack(pady=30)

    right_frame = ctk.CTkScrollableFrame(app, corner_radius=15, fg_color="#2b2b2b", width=400)
    right_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
    ctk.CTkLabel(right_frame, text="📜 Quick Command Guide", font=("Arial", 22, "bold"), text_color="#FFB6C1").pack(pady=(10, 20))

    def add_command_section(title, commands):
        ctk.CTkLabel(right_frame, text=title, font=("Arial", 16, "bold"), text_color="#00FFFF", anchor="w").pack(fill="x", padx=10, pady=(10, 5))
        for cmd in commands:
            ctk.CTkLabel(right_frame, text=f"• {cmd}", font=("Arial", 14), text_color="white", anchor="w", justify="left").pack(fill="x", padx=20, pady=3)

    add_command_section("⚠️ Rules:", [
        "🗣️ Language: Pihu understands pure Hinglish & English.",
        "❌ Press 'Esc' to exit Fullscreen."
    ])
    add_command_section("💻 PC Controls:", ["System status check", "Battery status", "Volume up / Volume down", "Mute"])
    add_command_section("🎵 Media Controls:", ["Pause video", "Resume play", "Next track / Previous track"])
    add_command_section("🌐 Internet & Apps:", ["YouTube open karo", "Chrome open", "Notepad start", "Ask any general question"])
    
    app.mainloop()

# --- 3. PYGAME AVATAR LOGIC ---
def start_pihu_avatar():
    global SUB_USER, SUB_PIHU
    
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Pihu AI")
    clock = pygame.time.Clock()

    try:
        font = pygame.font.SysFont("segoeui", 22, bold=True)
    except:
        font = pygame.font.Font(None, 22)

    def load_avatar_image(filename):
        try:
            path = get_path(f"assets/avatar/{filename}.png")
            img = pygame.image.load(path)
            orig_w, orig_h = img.get_size()
            scale = min(WIDTH / orig_w, HEIGHT / orig_h) 
            return pygame.transform.smoothscale(img, (int(orig_w * scale), int(orig_h * scale))), int(orig_w * scale), int(orig_h * scale)
        except:
            return pygame.Surface((500, 600)), 500, 600

    idle, av_w, av_h = load_avatar_image("idle")
    blink, _, _ = load_avatar_image("blink")
    talk1, _, _ = load_avatar_image("talk1")
    talk2, _, _ = load_avatar_image("talk2")
    talk_frames = [talk1, talk2]
    
    try: 
        magic_bg_color = idle.get_at((5, 5)) 
    except: 
        magic_bg_color = (20, 24, 33) 
        
    av_x = (WIDTH - av_w) // 2
    av_y = (HEIGHT - av_h) // 2

    def pihu_loop():
        global CURRENT_USER, SUB_USER, SUB_PIHU 
        
        time.sleep(0.5)
        SUB_PIHU = f"Hello Boss! Welcome back, main bilkul ready hu."
        speak(SUB_PIHU)

        while True:
            SUB_USER = "🎤 (Listening...)"
            u = listen()
            
            if u:
                SUB_USER = u  
                # सीधा AI इंजन प्रोसेस करेगा (कोई पुराना handle_command बीच में दखल नहीं देगा)
                reply = chat_with_pihu(u)
                if reply:
                    SUB_PIHU = reply 
                    speak(reply)
            else:
                SUB_USER = "..."
                time.sleep(0.3)

    threading.Thread(target=pihu_loop, daemon=True).start()

    blink_timer = time.time()
    talk_timer = time.time()
    talk_idx = 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit(0)

        screen.fill(magic_bg_color)

        if core.voice.is_speaking:
            if time.time() - talk_timer > 0.2:
                talk_idx = (talk_idx + 1) % len(talk_frames)
                talk_timer = time.time()
            current_avatar = talk_frames[talk_idx]
        else:
            current_avatar = idle
            if time.time() - blink_timer > 4:
                current_avatar = blink
                if time.time() - blink_timer > 4.3:
                    blink_timer = time.time()

        screen.blit(current_avatar, (av_x, av_y))

        # सबटाइटल बॉक्स
        rect_height = 80
        overlay = pygame.Surface((WIDTH, rect_height))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, HEIGHT - rect_height))

        user_surface = font.render(f"🗣️ You: {SUB_USER}", True, (0, 255, 255))
        screen.blit(user_surface, (30, HEIGHT - 70))

        pihu_surface = font.render(f"🤖 Pihu: {SUB_PIHU}", True, (255, 255, 0))
        screen.blit(pihu_surface, (30, HEIGHT - 35))

        pygame.display.flip()
        clock.tick(20)

if __name__ == "__main__":
    show_intro_screen()
    start_pihu_avatar()