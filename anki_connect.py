import json
import urllib.request
import urllib.error



def singleton(cls):
    _instance = {}

    def inner(**params):
        if cls not in _instance:
            _instance[cls] = cls(**params)
        return _instance[cls]

    return inner


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, **params):
    request_json = json.dumps(request(action, **params), ensure_ascii=False).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', request_json)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        # raise Exception(response['error'])
        pass
    return response


def check_connection():
    try:
        urllib.request.urlopen("http://localhost:8765")
    except WindowsError as e:
        return False
    return True


def get_model_fields(model_name):
    result = invoke("modelFieldNames", modelName=model_name)
    return result


def get_deck_name():
    return invoke("deckNames")["result"]


def create_deck(deck_name: str):
    existing_deck = invoke('deckNames')
    if deck_name in existing_deck:
        raise Exception('Deck {} has already existed.')
    else:
        invoke('createDeck', deck=deck_name)


def create_note_type(model_name: str, fields: list):
    action = "createModel"
    params = {
        "modelName": model_name,
        "inOrderFields": fields,
    }
    request_json = json.dumps(request(action, **params), ensure_ascii=False).encode('utf-8')
    pass


def add_note(note):
    result = invoke("addNote", note=note)
    return result


def add_notes(notes):
    result = invoke("addNotes", notes=notes)
    return result
