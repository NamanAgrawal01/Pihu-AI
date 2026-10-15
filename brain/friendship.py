import random

def get_friendship_reply(user_input):
    replies = [
        "Sahi kaha Hemant! Main toh hamesha tumhari baat sunne ke liye taiyaar hoon.",
        "Dost ho tum mere, batao aur kya chal raha hai?",
        "Mujhe achha lagta hai jab tum mujhse aise baatein karte ho.",
        "Sach mein? Ye toh bahut interesting hai!",
        "Tumhare saath baatein karke mera din ban jata hai."
    ]
    return random.choice(replies)