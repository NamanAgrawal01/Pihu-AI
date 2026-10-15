import cv2
import time
import os
import sys

class PihuEyesLite:
    def __init__(self):
        # 🌟 FIX 1: .exe के लिए एकदम पक्का (Absolute) पाथ
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))
            
        xml_path = os.path.join(base_path, 'haarcascade_frontalface_default.xml')
        
        # XML फाइल लोड करना
        self.face_cascade = cv2.CascadeClassifier(xml_path)
        
    def scan_for_human(self):
        # 🌟 FIX 2: cv2.CAP_DSHOW विंडोज़ .exe में कैमरे को ब्लॉक होने से रोकता है!
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            # अगर DSHOW काम न करे, तो नॉर्मल ट्राई करो
            cap = cv2.VideoCapture(0) 
            
        if not cap.isOpened():
            raise Exception("OpenCV कैमरे को चालू नहीं कर पा रहा है!")
            
        start_time = time.time()
        human_found = False
        
        while time.time() - start_time < 3:  # 3 सेकंड तक स्कैन
            ret, frame = cap.read()
            if not ret:
                break
                
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # चेहरा ढूँढना
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                human_found = True
                break
                
        cap.release()
        return human_found