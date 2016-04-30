import requests

# http://api.funtranslations.com/translate/yoda.json?text=
def translate(msg):
    r = requests.get("http://api.funtranslations.com/translate/yoda.json?text=" + msg)
    if r.status_code == 429:
        return "Sorry I can only translate 5 times per hour"
    try:
        return r.json()['contents']['translated'].replace("  ", " ")
    except:
        print(r.text)
        return "An unexpected error occured"

def run(thorin, incoming):
    return translate(incoming.message.text[incoming.message.text.index("yoda") + 5:])
