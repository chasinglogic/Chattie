import requests
from os import getenv

JENKINS_URL = getenv("THORIN_JENKINS_URL")
JENKINS_TOKEN = getenv("THORIN_JENKINS_TOKEN")

def run_build(strarr):
    build = strarr[strarr.index("build") + 1]
    r = requests.post(JENKINS_URL + "job/" + build + "/build?token=" + JEKNINS_TOKEN) 

def run(thorin, incoming):
    split = incoming.message.text.split(" ")
    return run_build(split)
