import os

def run(thorin, incoming):
    try:
        available_commands = [ f for f in os.listdir("./commands") if f.endswith(".py") and f != "__init__.py" ]
        return "I know:\n" + "\n".join(map(lambda x: x[:-3], available_commands))
    except:
        return "Sorry, there's no helping you."
