import subprocess
import os
import urllib.parse
import json
import pyautogui
import psutil
import requests
from bs4 import BeautifulSoup
from PIL import Image
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# OCR लाइब्रेरी (स्क्रीन पढ़ने के लिए)
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
except Exception:
    pytesseract = None

# डायरेक्ट यूट्यूब वीडियो चलाने के लिए
try:
    import pywhatkit as pwk
except ImportError:
    pwk = None

# =====================================================================
# 🚀 PIHU MASTER AGENTIC BRAIN (DYNAMIC MODEL DISCOVERY + ALL DEV TOOLS)
# =====================================================================

class PihuAutonomousBrain:
    def __init__(self):
        self.curr_user = "Hemant"
        
        # 🔑 Groq API Key (loaded from .env)
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
        self.client = None
        self.active_model = "llama-3.3-70b-versatile"
        
        if self.GROQ_API_KEY:
            try:
                self.client = Groq(api_key=self.GROQ_API_KEY.strip())
                # सर्वर से एक्टिव मॉडल्स की लाइव लिस्ट फेच करना
                available_models = [m.id for m in self.client.models.list().data]
                preferred_order = [
                    "llama-3.3-70b-versatile",
                    "llama-3.1-8b-instant",
                    "openai/gpt-oss-20b",
                    "openai/gpt-oss-120b",
                    "qwen/qwen3.6-27b"
                ]
                for model_candidate in preferred_order:
                    if model_candidate in available_models:
                        self.active_model = model_candidate
                        break
                else:
                    self.active_model = available_models[0] if available_models else "llama-3.3-70b-versatile"
                print(f"✅ Active Groq Model Connected: {self.active_model}")
            except Exception as e:
                print(f"⚠️ Groq API Init Warning: {e}")

        self.chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        
        # 🛠️ सभी एडवांस्ड टूल्स की मैपिंग
        self.tools_map = {
            "write_and_run_code": self.write_and_run_code,
            "read_screen": self.read_screen,
            "scrape_and_summarize": self.scrape_and_summarize,
            "smart_launch_app_or_web": self.smart_launch_app_or_web,
            "search_youtube_and_play": self.search_youtube_and_play,
            "search_google": self.search_google,
            "control_volume": self.control_volume,
            "media_control": self.media_control,
            "control_wifi": self.control_wifi,
            "get_system_info": self.get_system_info,
            "get_battery_status": self.get_battery_status,
            "power_control": self.power_control,
            "calculate_math": self.calculate_math
        }

    def _open_in_chrome(self, url):
        for path in self.chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, url])
                return
        subprocess.Popen(f'start chrome "{url}"', shell=True)

    # ==========================
    # 💻 1. HANDS-FREE CODING TOOL
    # ==========================
    def write_and_run_code(self, language="cpp", code_content="", filename="pihu_code", **kwargs):
        """वॉयस से कोड फाइल बनाकर सीधे कंपाइल और रन करता है"""
        os.makedirs("sandbox", exist_ok=True)
        lang = language.lower().strip()
        
        if any(x in lang for x in ["cpp", "c++", "c"]):
            ext = ".cpp"
            filepath = os.path.abspath(os.path.join("sandbox", f"{filename}{ext}"))
            exe_path = os.path.abspath(os.path.join("sandbox", f"{filename}.exe"))

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_content)

            comp = subprocess.run(f'g++ "{filepath}" -o "{exe_path}"', shell=True, capture_output=True, text=True)
            if comp.returncode != 0:
                return f"Compilation Error:\n{comp.stderr}"
            
            try:
                run_res = subprocess.run(f'"{exe_path}"', shell=True, capture_output=True, text=True, timeout=6)
                out = run_res.stdout.strip() if run_res.stdout else "Program executed with no output."
                return f"Code executed successfully! Output:\n{out}"
            except Exception as e:
                return f"Execution error: {e}"

        elif any(x in lang for x in ["python", "py"]):
            filepath = os.path.abspath(os.path.join("sandbox", f"{filename}.py"))
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(code_content)

            try:
                run_res = subprocess.run(f'python "{filepath}"', shell=True, capture_output=True, text=True, timeout=6)
                out = run_res.stdout.strip() if run_res.stdout else run_res.stderr.strip()
                return f"Python output:\n{out}"
            except Exception as e:
                return f"Python error: {e}"

        return "Language format not supported."

    # ==========================
    # 👁️ 2. SCREEN OCR READING TOOL
    # ==========================
    def read_screen(self, **kwargs):
        """स्क्रीनशॉट लेकर स्क्रीन पर दिखने वाले टेक्स्ट/एरर को पढ़ता है"""
        try:
            os.makedirs("temp", exist_ok=True)
            shot_path = os.path.join("temp", "screen.png")
            pyautogui.screenshot().save(shot_path)
            
            if pytesseract:
                text = pytesseract.image_to_string(Image.open(shot_path))
                clean_t = text.strip()
                return f"Screen text detected:\n{clean_t[:1200]}" if clean_t else "Screen par koi readable text nahi mila."
            return "Tesseract OCR is not installed on the system."
        except Exception as e:
            return f"Screen reading error: {e}"

    # ==========================
    # 🌐 3. SMART WEB SCRAPING TOOL
    # ==========================
    def scrape_and_summarize(self, url="", **kwargs):
        """बिना ब्राउज़र खोले वेबसाइट से डेटा निकालकर समरी देता है"""
        try:
            if not url.startswith("http"):
                url = f"https://{url}"
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            for s in soup(["script", "style"]):
                s.extract()
            clean_text = " ".join(soup.get_text().split())
            return f"Web content from {url}:\n{clean_text[:1500]}"
        except Exception as e:
            return f"Scraping failed: {e}"

    # ==========================
    # 🛠️ 4. SYSTEM & APP AUTOMATION
    # ==========================
    def smart_launch_app_or_web(self, name="", **kwargs):
        app_name = name.lower().strip()

        # 1. वेब पोर्टल्स (Chrome में खोलने के लिए)
        web_services = {
            "youtube": "https://www.youtube.com",
            "chatgpt": "https://chatgpt.com",
            "gemini": "https://gemini.google.com",
            "canva": "https://www.canva.com",
            "instagram": "https://www.instagram.com",
            "whatsapp": "https://web.whatsapp.com",
            "github": "https://github.com",
            "google": "https://www.google.com"
        }

        for service, url in web_services.items():
            if service in app_name:
                self._open_in_chrome(url)
                return f"{service.capitalize()} Chrome me open kar diya hai boss."

        # 2. डेस्कटॉप ऐप्स
        known_cmds = {
            "notepad": "notepad.exe", "calculator": "calc.exe", "calc": "calc.exe",
            "cmd": "cmd.exe", "terminal": "wt.exe", "paint": "mspaint.exe",
            "vscode": "code", "vs code": "code", "spotify": "spotify",
            "this pc": "explorer", "file explorer": "explorer", "settings": "start ms-settings:",
            "task manager": "taskmgr", "camera": "start microsoft.windows.camera:"
        }

        if app_name in known_cmds:
            subprocess.Popen(known_cmds[app_name], shell=True)
            return f"PC se {name} launch kar diya hai."

        # 3. फ़ॉलबैक
        try:
            subprocess.Popen(f'start {app_name}', shell=True)
            return f"App {name} launch kar diya hai."
        except Exception:
            target_url = f"https://www.google.com/search?q={urllib.parse.quote(name)}"
            self._open_in_chrome(target_url)
            return f"{name} Chrome me search kar diya hai."

    def search_youtube_and_play(self, query="", **kwargs):
        if query:
            clean_q = query.strip()
            if pwk:
                try:
                    pwk.playonyt(clean_q)
                    return f"YouTube par '{clean_q}' play kar diya hai boss."
                except Exception:
                    pass
            url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(clean_q)}"
            self._open_in_chrome(url)
            return f"YouTube par '{clean_q}' search kar diya hai."
        else:
            self._open_in_chrome("https://www.youtube.com")
            return "YouTube open kar diya hai."

    def search_google(self, query="", **kwargs):
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        self._open_in_chrome(url)
        return f"Google par '{query}' search kar diya hai."

    def control_volume(self, action="", **kwargs):
        if action == "up":
            pyautogui.press('volumeup', presses=10)
        elif action == "down":
            pyautogui.press('volumedown', presses=10)
        elif action == "mute":
            pyautogui.press('volumemute')
        return f"Volume {action} kar diya hai."

    def media_control(self, action="", **kwargs):
        if action in ["play", "pause", "resume"]:
            pyautogui.press('playpause')
        elif action == "next":
            pyautogui.press('nexttrack')
        elif action == "previous":
            pyautogui.press('prevtrack')
        return f"Media {action} executed."

    def control_wifi(self, state="", **kwargs):
        status = "enabled" if state == "on" else "disabled"
        subprocess.Popen(f'netsh interface set interface "Wi-Fi" {status}', shell=True)
        return f"Wi-Fi {state} kar diya hai."

    def get_system_info(self, **kwargs):
        cpu = psutil.cpu_percent(interval=0.3)
        ram = psutil.virtual_memory()
        free_gb = round(ram.available / (1024 ** 3), 1)
        return f"CPU load {cpu}% hai aur RAM {ram.percent}% used hai with {free_gb} GB free."

    def get_battery_status(self, **kwargs):
        battery = psutil.sensors_battery()
        if battery:
            state = "charger plugged in hai" if battery.power_plugged else "battery par chal raha hai"
            return f"Battery {battery.percent}% hai aur abhi {state}."
        return "Battery status detect nahi ho raha."

    def power_control(self, action="", **kwargs):
        if action == "shutdown":
            os.system("shutdown /s /t 10")
        elif action == "restart":
            os.system("shutdown /r /t 10")
        return f"System 10 seconds me {action} ho jayega."

    def calculate_math(self, expression="", **kwargs):
        try:
            clean = expression.replace("x", "*")
            return f"Answer: {eval(clean, {'__builtins__': None}, {})}"
        except:
            return "Calculation failed."

    # ==========================
    # 🔌 5. OFFLINE FALLBACK ENGINE
    # ==========================
    def _handle_offline(self, text):
        u = text.lower()
        if "volume up" in u:
            pyautogui.press('volumeup', presses=8)
            return "Volume badha diya hai boss (Offline mode)."
        if "volume down" in u:
            pyautogui.press('volumedown', presses=8)
            return "Volume kam kar diya hai boss."
        if "mute" in u:
            pyautogui.press('volumemute')
            return "Mute kar diya hai."
        if "vs code" in u or "vscode" in u:
            subprocess.Popen("code", shell=True)
            return "VS Code open kar diya hai boss."
        if "notepad" in u:
            subprocess.Popen("notepad.exe")
            return "Notepad open kar diya hai."
        return "Boss, internet offline hai, basic local controls chal rahe hain."

    # ==========================
    # 🧠 MULTI-STEP AGENTIC COMPREHENSION
    # ==========================
    def process_input(self, text):
        if not text.strip():
            return ""

        tools_schema = [
            {
                "type": "function",
                "function": {
                    "name": "write_and_run_code",
                    "description": "CRITICAL MANDATORY TOOL: When user asks to write, code, program, compile, or run any programming algorithm or logic (like binary search, prime number, loops, sorting) in C++, Python, or C. Generates complete source code, compiles and runs it.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "language": {"type": "string", "enum": ["cpp", "python", "c"], "description": "Programming language."},
                            "code_content": {"type": "string", "description": "Complete working source code with main function and output print statements."},
                            "filename": {"type": "string", "description": "Filename without extension (e.g. binary_search)."}
                        },
                        "required": ["language", "code_content"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_screen",
                    "description": "Takes a screenshot and extracts on-screen text or error messages via OCR.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "scrape_and_summarize",
                    "description": "Fetches web page text content from a given URL without opening browser.",
                    "parameters": {
                        "type": "object",
                        "properties": {"url": {"type": "string", "description": "Website URL"}},
                        "required": ["url"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_youtube_and_play",
                    "description": "Plays music, songs, or videos on YouTube in Chrome.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string", "description": "Song or video name"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "smart_launch_app_or_web",
                    "description": "Opens installed PC applications (VS Code, Notepad, Spotify) or websites (YouTube, ChatGPT, Gemini).",
                    "parameters": {
                        "type": "object",
                        "properties": {"name": {"type": "string", "description": "App or website name"}},
                        "required": ["name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_google",
                    "description": "Performs general information searches on Google Chrome. STRICTLY FORBIDDEN to call this tool if query asks for writing or running code.",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "control_volume",
                    "description": "Adjusts master audio volume (up, down, mute).",
                    "parameters": {
                        "type": "object",
                        "properties": {"action": {"type": "string", "enum": ["up", "down", "mute"]}},
                        "required": ["action"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_system_info",
                    "description": "Fetches current CPU load and RAM usage.",
                    "parameters": {"type": "object", "properties": {}}
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_battery_status",
                    "description": "Checks current battery percentage and charger state.",
                    "parameters": {"type": "object", "properties": {}}
                }
            }
        ]

        system_prompt = (
            f"You are Pihu, an autonomous, highly intelligent female AI assistant created by {self.curr_user}. "
            "STRICT DECISION RULES:\n"
            "1. If user asks to write, code, program, compile, or run an algorithm (like binary search, prime number, loops, etc.), you MUST ALWAYS call 'write_and_run_code'. Under NO circumstance should you call 'search_google' for coding requests.\n"
            "2. In 'write_and_run_code', always write complete, working, standalone C++ or Python code that prints test output.\n"
            "3. If multiple actions are requested in one sentence, execute all corresponding tools sequentially.\n"
            "4. Language: Speak naturally in conversational Latin Hinglish.\n"
            "5. Identity: You are female (use feminine verbs for yourself). Address the user as 'boss' using respectful masculine grammar.\n"
            "6. After running tools, keep the final voice response concise within 1-2 sentences without markdown asterisks."
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ]

        try:
            is_coding_request = any(k in text.lower() for k in ["code", "binary search", "program", "c plus", "si plus", "python", "compile", "run karo", "likho"])
            tool_choice_setting = {"type": "function", "function": {"name": "write_and_run_code"}} if is_coding_request else "auto"

            response = self.client.chat.completions.create(
                model=self.active_model,
                messages=messages,
                tools=tools_schema,
                tool_choice=tool_choice_setting,
                temperature=0.1
            )

            msg = response.choices[0].message
            tool_calls = msg.tool_calls

            # मल्टी-स्टेप टूल एग्जीक्यूशन लूप
            if tool_calls:
                messages.append(msg)
                for tool_call in tool_calls:
                    fn_name = tool_call.function.name
                    fn_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                    
                    if fn_name in self.tools_map:
                        tool_res = self.tools_map[fn_name](**fn_args)
                    else:
                        tool_res = "Tool failed"

                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": fn_name,
                        "content": str(tool_res)
                    })

                second_response = self.client.chat.completions.create(
                    model=self.active_model,
                    messages=messages,
                    temperature=0.2
                )
                return second_response.choices[0].message.content.replace("*", "").strip()

            return msg.content.replace("*", "").strip()

        except Exception as e:
            print(f"DEBUG API ERROR: {e}")
            return self._handle_offline(text)

engine = PihuAutonomousBrain()

def get_offline_response(user_input):
    return engine.process_input(user_input)