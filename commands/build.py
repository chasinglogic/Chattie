import requests
from os import getenv

JENKINS_URL = getenv("THORIN_JENKINS_URL")
JENKINS_TOKEN = getenv("THORIN_JENKINS_TOKEN")

def run_build(strarr):
    r = requests.post(JENKINS_URL + "/job/" + strarr[strarr.index("build") + 1] + "/build?token=" + JEKNINS_TOKEN) 
    if r.status_code > 300:
        print("Error with the request:", r.text)
        return "I couldn't start the build."
    else:
        return "Build successfully started."

def run(thorin, incoming):
    split = incoming.message.text.split(" ")
    return run_build(split)
