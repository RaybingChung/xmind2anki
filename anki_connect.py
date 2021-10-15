import json
import urllib.request
import urllib.error
from typing import List


def singleton(cls):
    _instance = {}

    def inner(**params):
        if cls not in _instance:
            _instance[cls] = cls(**params)
        return _instance[cls]

    return inner


@singleton
class AnkiConnector:
    def __init__(self, deck_name="Default", model_name='Basic'):
        self.deck_name = deck_name
        self.model_name = model_name

    unsent_notes = []

    def request(self, action, **params):
        return {'action': action, 'params': params, 'version': 6}

    def invoke(self, action, **params):
        request_json = json.dumps(self.request(action, **params), ensure_ascii=False).encode('utf-8')
        response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', request_json)))
        if len(response) != 2:
            raise Exception('response has an unexpected number of fields')
        if 'error' not in response:
            raise Exception('response is missing required error field')
        if 'result' not in response:
            raise Exception('response is missing required result field')
        if response['error'] is not None:
            raise Exception(response['error'])
        return response

    def check_connection(self):
        try:
            urllib.request.urlopen("http://localhost:8765")
        except WindowsError as e:
            return False
        return True

    def get_model_fields(self, model_name):
        result = self.invoke("modelFieldNames", modelName=model_name)
        return result

    def get_deck_name(self):
        return self.invoke("deckNames")["result"]

    def create_deck(self, deck_name: str):
        existing_deck = self.invoke('deckNames')
        if deck_name in existing_deck:
            raise Exception('Deck {} has already existed.')
        else:
            self.invoke('createDeck', deck=deck_name)

    def create_note_type(self, model_name: str, fields: list):
        action = "createModel"
        params = {
            "modelName": model_name,
            "inOrderFields": fields,
        }
        request_json = json.dumps(self.request(action, **params), ensure_ascii=False).encode('utf-8')
        pass

    def check_note_and_field(self, model_name: str):
        pass

    def update_card_template(self):
        pass

    def assembly_note(self, note):
        tags: List[str] = note["tags"]
        tags = [tag.replace(' ', '_') for tag in tags]
        del note["tags"]
        return {
            "deckName": self.deck_name,
            "modelName": self.model_name,
            "tags": tags,
            "fields": note
        }

    def add_note(self, note):
        note = self.assembly_note(note)
        result = self.invoke("addNote", note=note)
        return result

    def add_notes(self):
        notes = [self.assembly_note(note) for note in self.unsent_notes]
        result = self.invoke("addNotes", notes=notes)
        self.unsent_notes.clear()
        return result