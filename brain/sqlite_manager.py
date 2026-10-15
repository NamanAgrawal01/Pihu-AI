import sqlite3
import json
import os

class PihuDatabase:
    def __init__(self, db_name="data/pihu_ai.db"):
        os.makedirs("data", exist_ok=True)
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._setup_tables()
        self._auto_migrate_old_data() # 👈 यह पुरानी फाइल को SQL में बदल देगा!

    def _setup_tables(self):
        # प्रोफाइल और रिश्तों के लिए टेबल
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS user_profile 
                            (user TEXT, key TEXT, value TEXT, PRIMARY KEY(user, key))''')
        # डायरी/यादों के लिए टेबल
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS memories 
                            (user TEXT, memory TEXT)''')
        self.conn.commit()

    def _auto_migrate_old_data(self):
        json_file = 'data/pihu_memory.json'
        backup_file = 'data/pihu_memory_backup.json'
        
        if os.path.exists(json_file):
            print("🔄 पुरानी JSON फाइल से डेटा SQL में ट्रांसफर हो रहा है...")
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # हर यूज़र का डेटा SQL में डालो
                    for user, p_data in data.get("users", {}).items():
                        # रिश्ते माइग्रेट करना
                        for k, v in p_data.get("relations", {}).items():
                            self.save_profile(user, f"rel_{k}", v)
                        # उदासी का कारण
                        if "last_sad_reason" in p_data:
                            self.save_profile(user, "last_sad_reason", p_data["last_sad_reason"])
                        # डायरी/मेमोरी
                        for mem in p_data.get("memories", []):
                            self.save_memory(user, mem)
                            
                # डेटा ट्रांसफर होने के बाद पुरानी फाइल का नाम बदल दो ताकि बार-बार रन न हो
                os.rename(json_file, backup_file)
                print("✅ 100% डेटा सुरक्षित तरीके से SQL में आ गया है!")
            except Exception as e:
                print(f"⚠️ ट्रांसफर में छोटी सी दिक्कत: {e}")

    def save_profile(self, user, key, value):
        self.cursor.execute('INSERT OR REPLACE INTO user_profile VALUES (?, ?, ?)', (user, key, value))
        self.conn.commit()

    def get_profile(self, user, key):
        self.cursor.execute('SELECT value FROM user_profile WHERE user=? AND key=?', (user, key))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def save_memory(self, user, memory_text):
        self.cursor.execute('INSERT INTO memories VALUES (?, ?)', (user, memory_text))
        self.conn.commit()

    def get_last_memory(self, user):
        self.cursor.execute('SELECT memory FROM memories WHERE user=? ORDER BY rowid DESC LIMIT 1', (user,))
        result = self.cursor.fetchone()
        return result[0] if result else None