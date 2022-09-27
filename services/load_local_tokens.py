import json
from .connecting import obj


def load_tokens_auth():
    with open('config/tokens.json', 'r') as file:
        data = json.load(file)

    if data != {}:
        obj.xsrf = data['xsrf']
        obj.hhtoken = data['hhtoken']
