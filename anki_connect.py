import json
import urllib.request
import urllib.error
import datetime
import warnings


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
    warnings.simplefilter("always")
    failed_data = []
    if len(response) != 2:
        print(params)
        params['message'] = "One conversion failed due to an unexpected number of fields"
        failed_data.append(params)
        warn_print("One conversion failed due to an unexpected number of fields")
    if 'error' not in response:
        print(params)
        params['message'] = "One conversion failed due to missing required error field"
        failed_data.append(params)
        warn_print("One conversion failed due to missing required error field")
    if 'result' not in response:
        print(params)
        params['message'] = "One conversion failed due to missing required error field"
        failed_data.append(params)
        warn_print("One conversion failed due to missing required error field")
    if response['error'] is not None:
        print(params)
        params['message'] = response['error']
        failed_data.append(params)
        warn_print(response['error'])
    record_failed_data(failed_data)
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


def add_note(note):
    result = invoke("addNote", note=note)
    return result


def add_notes(notes):
    result = invoke("addNotes", notes=notes)
    return result


def record_failed_data(params):
    data_time = datetime.datetime
    with open('FailedData/failed_data' + data_time.now().strftime("%Y%m%d%H%m") + '.json', 'a+', encoding='utf8') as f:
        json.dump(params, f, ensure_ascii=False)


def warn_print(string):
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKCYAN = '\033[96m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    print(bcolors.FAIL + string + bcolors.ENDC)
