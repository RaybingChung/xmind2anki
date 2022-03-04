from typing import List

from xmind_parser import ParsedNodeFromXmind


class CvtMode:
    deck_name: str
    tags: List = ['xmind']
    models: List = ['基础']

    @classmethod
    def transform_node_to_note(cls, node: ParsedNodeFromXmind):
        front = node['title']

        for ancestor in reversed(node['ancestors']):
            front = ancestor + ' -> ' + front
        front = cls.__decorate_string(front)
        back = ''
        for child in node['children']:
            back = back + cls.__decorate_string(child)

        return cls.__make_note(fields=cls.__transform_to_common_note_fields(front, back),
                               deck_name=cls.deck_name, model_name=cls.models[0], tags=cls.tags)

    @staticmethod
    def __decorate_string(string: str):
        return '<div>' + string + '</div>'

    @staticmethod
    def __transform_to_common_note_fields(front, back):
        return {
            "正面": front,
            "背面": back
        }

    @staticmethod
    def __make_note(fields, deck_name: str, model_name: str, tags: List):
        return {
            "deckName": deck_name,
            "modelName": model_name,
            "tags": tags,
            "fields": fields
        }
