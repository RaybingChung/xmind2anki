import json
import zipfile
from copy import copy
from typing import List, TypedDict


class Node(TypedDict):
    title: str
    children: List[str]
    ancestors: List[str]


def load_xmind(path_to_file):
    with zipfile.ZipFile(path_to_file) as zip_out:
        with zip_out.open('content.json') as zip_file:
            file_content = zip_file.read()
    file_content = json.loads(file_content)
    file_content = file_content[0]['rootTopic']
    return file_content


def get_title(node):
    return node["title"]


def get_children_nodes(node):
    if "children" not in node:
        raise Exception('There is no child in {}'.format(get_title(node)))
    return node["children"]["attached"]


def get_children_titles(node):
    if "children" not in node:
        raise Exception('There is no child in {}'.format(get_title(node)))
    return [get_title(child) for child in get_children_nodes(node)]


# def traverse_nodes(xmind_file_path):
#     root = load_xmind(xmind_file_path)
#     unexplored_node = [root]
#     traversed_nodes: List[Node] = []
#
#     while len(unexplored_node) != 0:
#         current_node = unexplored_node[-1]
#         del unexplored_node[-1]
#
#         if 'children' not in current_node:
#             continue
#
#         for child_node in reversed(get_children_nodes(current_node)):
#             unexplored_node.append(child_node)
#         traversed_nodes.append({'title': get_title(current_node),
#                                 'children': get_children_titles(current_node),
#                                 'ancestors': []})
#     return traversed_nodes


def traverse_nodes_rem_path(xmind_file_path):
    # ancestors are directly added to the node object in the memory
    root = load_xmind(xmind_file_path)
    root['ancestors'] = []
    unexplored_node = [root]

    traversed_nodes_rem_path: List[Node] = []
    while len(unexplored_node) != 0:

        current_node = unexplored_node[-1]
        del unexplored_node[-1]

        if 'children' not in current_node:
            continue
        traversed_nodes_rem_path.append({'title': get_title(current_node),
                                         'children': get_children_titles(current_node),
                                         'ancestors': current_node['ancestors']})

        ancestors = copy(current_node['ancestors'])
        ancestors.append(get_title(current_node))

        for child_node in reversed(get_children_nodes(current_node)):
            child_node['ancestors'] = ancestors
            unexplored_node.append(child_node)

    return traversed_nodes_rem_path
