def run(chattie, incoming):
    try:
        target = incoming.message.text.split(" ")[incoming.message.text.split(" ").index("shots_fired") + 1]
        return "pew PEW pew " + target + " PEW pew PEW"
    except:
        return "pew pew PEW PEW PEW"
