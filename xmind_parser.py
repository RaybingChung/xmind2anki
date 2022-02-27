import json
import zipfile
from shutil import copyfile
from typing import List, TypedDict, Dict
from warnings import warn


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
                zip_file.write(bytes(json.dumps(xmind, ensure_ascii=False), 'utf-8'))


def get_root(xmind):
    return xmind[0]['rootTopic']


def get_hrefs(xmind):
    return [href['rootTopic'] for href in xmind[1:]]


def get_title_from_raw_node(raw_node):
    return raw_node["title"]


def get_children_nodes_from_raw_node(raw_node, hrefs):
    if "children" not in raw_node and 'href' not in raw_node:
        raise Exception('There is no child in {}'.format(get_title_from_raw_node(raw_node)))
    elif "children" in raw_node and 'href' in raw_node:
        warn('There are both href and children in {}'.format(str(raw_node)))
        # href_id = raw_node['href'].split('#')[-1]
        # for node in hrefs:
        #     if node['id'] == href_id:
        #         return node['children']['attached'] + raw_node['children']['attached']
        href_node = get_href_node(raw_node, hrefs)
        return href_node['children']['attached'] + raw_node['children']['attached']
    elif "children" not in raw_node and 'href' in raw_node:
        # href_id = raw_node['href'].split('#')[-1]
        # for node in hrefs:
        #     if node['id'] == href_id:
        #         return node['children']['attached']
        href_node = get_href_node(raw_node, hrefs)
        return href_node['children']['attached']
    else:
        return raw_node['children']['attached']


def get_href_node(current_raw_node: dict, hrefs):
    if 'href' not in current_raw_node:
        raise Exception('There is no href in this node {}'.format(str(current_raw_node)))
    href_id = current_raw_node['href'].split('#')[-1]
    # print(hrefs)
    for node in hrefs:
        # print(node['id'])
        if node['id'] == href_id:
            return node
    raise Exception('There is no specific id:{} node in hrefs of node {}'.format(href_id, str(current_raw_node)))


def get_children_titles_from_raw_node(raw_node, hrefs):
    if "children" not in raw_node and 'href' not in raw_node:
        raise Exception('There is no child in {}'.format(get_title_from_raw_node(raw_node)))
    if 'href' in raw_node:
        return [get_title_from_raw_node(child) for child in get_children_nodes_from_raw_node(raw_node, hrefs)]
    return [get_title_from_raw_node(child) for child in get_children_nodes_from_raw_node(raw_node, hrefs)]


def check_process_or_not_from_raw_node(raw_node: Dict):
    if 'markers' not in raw_node:
        return False
    else:
        for marker in raw_node['markers']:
            if marker['markerId'] == 'task-done':
                return True
        return False


def add_processed_marker(raw_node: Dict, hrefs):
    # print(raw_node)
    if 'href' in raw_node:
        href_node = get_href_node(raw_node, hrefs)
        add_processed_marker(href_node, hrefs)
    if 'markers' not in raw_node:
        raw_node['markers']: List = [{'markerId': "task-done"}]
    else:
        raw_node['markers'].append({'markerId': "task-done"})


def trans_raw_node2processed_node(raw_node, ancestors, hrefs):
    return {'title': get_title_from_raw_node(raw_node),
            'children': get_children_titles_from_raw_node(raw_node, hrefs),
            'ancestors': ancestors}


def traverse_nodes(xmind_file_path):
    xmind = load_xmind(xmind_file_path)
    root = get_root(xmind)
    hrefs = get_hrefs(xmind)

    ancestor_list_stack = [[]]
    raw_node_stack = [root]
    processed_node_stack = []

    while len(raw_node_stack) != 0:
        node = raw_node_stack.pop()
        current_title = get_title_from_raw_node(node)
        ancestors = ancestor_list_stack.pop()
        # print(node)
        if "children" in node or 'href' in node:
            if check_process_or_not_from_raw_node(node) is False:
                add_processed_marker(node, hrefs)
                processed_node_stack.append(trans_raw_node2processed_node(node, ancestors, hrefs))

            else:
                pass
            children = get_children_nodes_from_raw_node(node, hrefs)

            raw_node_stack.extend(reversed(children))
            children_ancestors = ancestors.copy()
            children_ancestors.append(current_title)
            ancestor_list_stack.extend([children_ancestors for _ in range(len(children))])

        else:
            if check_process_or_not_from_raw_node(node) is False:
                add_processed_marker(node, hrefs)
            else:
                pass
    # print(xmind)
    return processed_node_stack, xmind
