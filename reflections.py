reflections = {
    "i am": "you are",
    "i": "you",
    "me": "you",
    "my": "your",
    "you are": "I am",
    "you": "me",
    "your": "my"
}

def reflect(fragment):
    words = fragment.lower().split()
    return ' '.join([reflections.get(w, w) for w in words])