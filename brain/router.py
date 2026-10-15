from brain.friendship import get_friendship_reply
from brain.jokes import get_joke
from brain.motivation import get_motivation

def route_offline_query(user_input):
    u = user_input.lower()
    if any(x in u for x in ["joke", "chutkula", "hanso"]): return get_joke()
    if any(x in u for x in ["udaas", "sad", "motivate", "pareshan"]): return get_motivation()
    return get_friendship_reply(user_input)