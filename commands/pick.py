import random

def run(thorin, incoming):
    return choose(incoming.message.text) 

def choose(msg):
    split = msg.split(" ")
    choices = split[split.index("pick") + 1:]
    return choices[random.randrange(0, len(choices))]

if __name__ == "__main__":
    print(choose("@thorin_bot pick jason justin mat"))
