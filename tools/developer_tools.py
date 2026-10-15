import os
import subprocess
import requests
from bs4 import BeautifulSoup
import pyautogui
from PIL import Image

try:
    import pytesseract
    # Tesseract का डिफॉल्ट पाथ
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
except Exception:
    pytesseract = None

class DevTools:
    @staticmethod
    def read_screen():
        """स्क्रीनशॉट लेकर एरर या टेक्स्ट पढ़ता है"""
        try:
            os.makedirs("temp", exist_ok=True)
            shot_path = os.path.join("temp", "screen.png")
            screenshot = pyautogui.screenshot()
            screenshot.save(shot_path)
            
            if pytesseract:
                text = pytesseract.image_to_string(Image.open(shot_path))
                return f"Screen text detected:\n{text[:1000]}"
            return "Screen capture saved, but Tesseract OCR is not installed."
        except Exception as e:
            return f"Screen read error: {e}"

    @staticmethod
    def write_and_run_code(language, code_content, filename="test_code"):
        """कोड फाइल बनाकर सीधे कंपाइल/रन करता है"""
        os.makedirs("sandbox", exist_ok=True)
        ext_map = {"cpp": ".cpp", "c": ".c", "python": ".py", "java": ".java"}
        ext = ext_map.get(language.lower(), ".py")
        filepath = os.path.join("sandbox", f"{filename}{ext}")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code_content)

        try:
            if language.lower() in ["cpp", "c++"]:
                exe_path = os.path.join("sandbox", "a.exe")
                compile_res = subprocess.run(f"g++ {filepath} -o {exe_path}", shell=True, capture_output=True, text=True)
                if compile_res.returncode != 0:
                    return f"Compilation Error: {compile_res.stderr}"
                run_res = subprocess.run(exe_path, shell=True, capture_output=True, text=True, timeout=5)
                return f"Output: {run_res.stdout}"

            elif language.lower() == "python":
                run_res = subprocess.run(f"python {filepath}", shell=True, capture_output=True, text=True, timeout=5)
                return f"Output:\n{run_res.stdout}\nErrors:\n{run_res.stderr}"

            return "Language executed successfully."
        except Exception as e:
            return f"Execution error: {e}"

    @staticmethod
    def scrape_and_summarize(url):
        """बिना ब्राउज़र खोले वेबसाइट का टेक्स्ट निकालता है"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(res.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.extract()
            text = " ".join(soup.get_text().split())
            return text[:1500]
        except Exception as e:
            return f"Scraping error: {e}"