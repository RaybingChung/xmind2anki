import zipfile
import json
import urllib.request
from anki_connect import AnkiConnector


class XMindParser:
    def __init__(self, xmind_file_path=None):
        self.xmind_file_path = xmind_file_path

    unstashed_nodes = []

    def load_xmind(self, path_to_file):
        with zipfile.ZipFile(path_to_file) as zip_out:
            with zip_out.open('content.json') as zip_file:
                file_content = zip_file.read()
        file_content = json.loads(file_content)
        file_content = file_content[0]['rootTopic']
        return file_content

    def get_path(self, node):
        return node["path"]

    def get_note(self, node: dict):
        if "notes" not in node:
            raise Exception('There is no notes in {}'.format(self.get_title(node)))
        return node["notes"]["plain"]["content"]

    def get_title(self, node):
        return node["title"]

    def get_children_nodes(self, node):
        if "children" not in node:
            raise Exception('There is no child in {}'.format(self.get_title(node)))
        return node["children"]["attached"]

    def add_note_as_child(self, node):
        if "notes" not in node:
            raise Exception('There is no notes in {}'.format(self.get_title(node)))
        node["children"]["attached"].append({
            "title": self.get_note(node)
        })

    def get_children_titles(self, node):
        if "children" not in node:
            raise Exception('There is no child in {}'.format(self.get_title(node)))
        return [self.get_title(child) for child in self.get_children_nodes(node)]

    def traverse(self):
        unexplored_node = []
        path_to_current_node = []

        root = self.load_xmind(self.xmind_file_path)
        root['path'] = [self.get_title(root)]
        unexplored_node.append(root)

        # For test, there are 46 valid nodes.
        count = 0
        while len(unexplored_node) != 0:
            count = count + 1
            current_node = unexplored_node[-1]
            del unexplored_node[-1]
            if 'children' not in current_node:
                continue
            path_to_current_node.append(current_node)
            if "notes" in current_node:
                self.add_note_as_child(current_node)
            for child_node in self.get_children_nodes(current_node):
                child_node['path'] = current_node['path'][:]
                child_node['path'].append(self.get_title(child_node))
                unexplored_node.append(child_node)

            '''
                This is where to write the operation code for anki.
            '''
            self.unstashed_nodes.append(self.node_cvt_anki_note(current_node))
        return count

    def node_cvt_anki_note(self, node: dict):
        children = self.get_children_titles(node)
        children.append("notes")

        anki_note = {
            "Node": node["title"],
            "Anchestors": json.dumps(node["path"], ensure_ascii=False),
            "Children": json.dumps(self.get_children_titles(node), ensure_ascii=False),
            "tags": node["path"][:3]
        }
        return anki_note

    def get_unstashed_node(self):
        return self.unstashed_nodes

    def flush_nodes(self):
        self.unstashed_nodes.clear()


if __name__ == '__main__':
    xmind_parser = XMindParser("XmindFiles/成功类.xmind")
    anki_connector = AnkiConnector(deck_name='xmind2anki', model_name='SkeletonMemorizing')

    deck_to_save = "xmind2anki"

    count = xmind_parser.traverse()
    anki_connector.unsent_notes = xmind_parser.unstashed_nodes
    result = anki_connector.add_notes()


