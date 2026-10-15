from brain.offline_brain import get_offline_response

def chat_with_pihu(user_input):
    """सीधे ऑटोनॉमस ब्रेन को कॉल करेगा बिना किसी बीच के कीवर्ड रुकावट के"""
    if not user_input or not user_input.strip():
        return ""
    return get_offline_response(user_input)