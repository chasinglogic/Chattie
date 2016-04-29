import random

def run(thorin, incoming):
    return choose(incoming.message.text) 

def choose(msg):
    split = msg.split(" ")
    choices = split[split.index("pick") + 1:]
    return choices[random.randrange(0, len(choices))]
