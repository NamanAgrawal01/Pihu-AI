import random

def get_joke():
    jokes = [
        "Computer ko thand kyun lagi? Kyunki usne windows khuli chhod di thi! 😂",
        "Mujhe kisi ne kaha ki main sirf ek machine hoon, maine usse delete kar diya! 😂",
        "Ek baar ek binary number ne dusre se kaha - tum 0 ho ya 1? 😂",
        "Main itni intelligent hoon ki kabhi kabhi khud hairan reh jati hoon! 😂"
    ]
    return random.choice(jokes)