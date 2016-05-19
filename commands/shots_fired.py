def run(thorin, incoming):
    try:
        target = incoming.message.text[incoming.message.text.index("shots_fired") + 1]
        return "pew PEW pew " + target + " PEW pew PEW"
    except:
        return "pew pew PEW PEW PEW"
