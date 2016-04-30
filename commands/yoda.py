import requests

# http://api.funtranslations.com/translate/yoda.json?text=
def translate(msg):
    r = requests.get("http://api.funtranslations.com/translate/yoda.json?text=" + msg)
    try:
        return r.json()['contents']['translated'].replace("  ", " ")
    except:
        print(sys.exec_info()[1])
        return "An unexpected error occured"

def run(thorin, incoming):
    return translate(incoming.message.text[incoming.message.text.index("yoda") + 5:])
