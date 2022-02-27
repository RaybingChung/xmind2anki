import json
import zipfile
from shutil import copyfile
from typing import List, TypedDict, Dict


class ProcessedNode(TypedDict):
    title: str
    children: List[str]
    ancestors: List[str]


def create_backup_xmind_file(path_to_file: str):
    if path_to_file.split('.')[-1] != 'xmind':
        raise Exception('not xmind file')
    path_name = path_to_file.split(sep='.')
    path_name[-2] = path_name[-2] + '_backup'
    dst_path_to_file = '.'.join(path_name)
    copyfile(path_to_file, dst_path_to_file)
    return dst_path_to_file


def load_xmind(path_to_file: str):
    with zipfile.ZipFile(path_to_file) as zip_out:
        with zip_out.open('content.json') as zip_file:
            xmind = zip_file.read()

    xmind = json.loads(xmind)
    return xmind


def save_xmind(path_to_file, xmind):
    back_up_path = create_backup_xmind_file(path_to_file)

    with zipfile.ZipFile(back_up_path, mode='r') as zip_in:
        with zipfile.ZipFile(path_to_file, mode='w') as zip_out:
            # print(zip_in.infolist())
            for item in zip_in.infolist():
                if item.is_dir():
                    continue
                if item.filename == 'content.json':
                    continue
                buffer = zip_in.read(item)

                with zip_out.open(item, mode='w') as zip_file:
                    zip_file.write(buffer)
            with zip_out.open('content.json', mode='w') as zip_file:
                zip_file.write(bytes(json.dumps(xmind), 'utf-8'))


def get_root(xmind):
    return xmind[0]['rootTopic']


def get_hrefs(xmind):
    return [href['rootTopic'] for href in xmind][1:]


def get_title_from_raw_node(raw_node):
    return raw_node["title"]


def get_children_nodes_from_raw_node(raw_node):
    if "children" not in raw_node:
        raise Exception('There is no child in {}'.format(get_title_from_raw_node(raw_node)))
    return raw_node["children"]["attached"]


def get_children_titles_from_raw_node(raw_node):
    if "children" not in raw_node:
        raise Exception('There is no child in {}'.format(get_title_from_raw_node(raw_node)))
    return [get_title_from_raw_node(child) for child in get_children_nodes_from_raw_node(raw_node)]


def check_process_or_not_from_raw_node(raw_node: Dict):
    if 'markers' not in raw_node:
        return False
    else:
        for marker in raw_node['markers']:
            if marker['markerId'] == 'task-done':
                return True
        return False


def add_processed_marker(raw_node: Dict):
    if 'markers' not in raw_node:
        raw_node['markers']: List = [{'markerId': "task-done"}]
    else:
        raw_node['markers'].append({'markerId': "task-done"})


def tran_node_raw2process(raw_node, ancestors):
    # print(ancestors)
    return {'title': get_title_from_raw_node(raw_node),
            'children': get_children_titles_from_raw_node(raw_node),
            'ancestors': ancestors}


def traverse_nodes(xmind_file_path):
    xmind = load_xmind(xmind_file_path)
    root = get_root(xmind)

    ancestor_list_stack = [[]]
    raw_node_stack = [root]
    processed_node_stack = []

    while len(raw_node_stack) != 0:
        node = raw_node_stack.pop()
        current_title = get_title_from_raw_node(node)
        ancestors = ancestor_list_stack.pop()
        # print(current_title)
        if 'children' in node:
            if check_process_or_not_from_raw_node(node) is False:
                add_processed_marker(node)
                processed_node_stack.append(tran_node_raw2process(node, ancestors))
                # print(ancestors)
            else:
                pass
            children = get_children_nodes_from_raw_node(node)

            raw_node_stack.extend(reversed(children))
            children_ancestors = ancestors.copy()
            children_ancestors.append(current_title)
            ancestor_list_stack.extend([children_ancestors for i in range(len(children))])

        else:
            if check_process_or_not_from_raw_node(node) is False:
                add_processed_marker(node)
            else:
                pass
    return processed_node_stack, xmind
