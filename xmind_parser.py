import json
import zipfile
from os import sep, mkdir
from os.path import exists
from shutil import copyfile
from time import strftime, localtime
from typing import List, TypedDict, Dict
from warnings import warn


class ProcessedNode(TypedDict):
    title: str
    children: List[str]
    ancestors: List[str]


class NodeStatus:
    unsaved = 'unsaved'
    saved = 'saved'
    updated = 'updated'


class XmindParser:
    xmind_file_path: str
    xmind_json = None
    xmind_file_path: str
    back_up_dir_path: str
    root = None
    hrefs = None
    parsed_notes = None

    def __init__(self, xmind_file_path, back_up_path=None):
        self.xmind_file_path = xmind_file_path
        self.xmind_json = self.load_xmind()
        if back_up_path is not None:
            self.back_up_dir_path = back_up_path
        self.root = self.get_root()
        self.hrefs = self.get_hrefs()
        # print(self.hrefs)
        self.parsed_notes = self.parse_xmind()

    def load_xmind(self):
        with zipfile.ZipFile(self.xmind_file_path) as zip_out:
            with zip_out.open('content.json') as zip_file:
                xmind_json = zip_file.read()
        xmind_json = json.loads(xmind_json)

        return xmind_json

    def create_backup_xmind_file(self):
        if self.xmind_file_path.split('.')[-1] != 'xmind':
            raise Exception('not xmind file')

        path_name = self.xmind_file_path.split(sep='.')
        path_name[-2] = path_name[-2] + '_backup_' + strftime('%Y%M%D%H', localtime())

        dst_path_to_file = '.'.join(path_name)
        if self.back_up_dir_path is not None:
            if exists(self.back_up_dir_path) is None:
                mkdir(self.back_up_dir_path)
            dst_path_to_file = '.'.join([self.back_up_dir_path, dst_path_to_file.split(sep)[-1]])
        copyfile(self.xmind_file_path, dst_path_to_file)
        return dst_path_to_file

    def save_xmind_to_file(self):
        back_up_file_path = self.create_backup_xmind_file()

        with zipfile.ZipFile(back_up_file_path, mode='r') as zip_in:
            with zipfile.ZipFile(self.xmind_file_path, mode='w') as zip_out:
                for item in zip_in.infolist():
                    if item.is_dir():
                        continue
                    if item.filename == 'content.json':
                        continue
                    buffer = zip_in.read(item)

                    with zip_out.open(item, mode='w') as zip_file:
                        zip_file.write(buffer)
                with zip_out.open('content.json', mode='w') as zip_file:
                    zip_file.write(bytes(json.dumps(self.xmind_json, ensure_ascii=False), 'utf-8'))

    def get_root(self):
        if self.root is not None:
            return self.root
        return self.xmind_json[0]['rootTopic']

    def get_hrefs(self):
        if self.hrefs is not None:
            return self.hrefs
        return [href['rootTopic'] for href in self.xmind_json[1:]]

    @staticmethod
    def get_title_from_xmind_node(xmind_node):
        return xmind_node["title"]

    @staticmethod
    def get_id_from_xmind_node(xmind_node):
        return xmind_node["id"]

    def get_children_nodes_from_xmind_node(self, xmind_node):
        if "children" not in xmind_node and 'href' not in xmind_node:
            raise Exception('There is no child in {}'.format(self.get_title_from_xmind_node(xmind_node)))
        elif "children" in xmind_node and 'href' in xmind_node:
            warn('There are both href and children in {}'.format(str(xmind_node)))
            href_node = self.get_href_of_node_in_new_sheet(xmind_node)
            return href_node['children']['attached'] + xmind_node['children']['attached']
        elif "children" not in xmind_node and 'href' in xmind_node:
            href_node = self.get_href_of_node_in_new_sheet(xmind_node)
            return href_node['children']['attached']
        else:
            return xmind_node['children']['attached']

    def get_href_of_node_in_new_sheet(self, current_raw_node: dict):
        if 'href' not in current_raw_node:
            raise Exception('There is no href in this node {}'.format(str(current_raw_node)))
        href_id = current_raw_node['href'].split('#')[-1]
        for node in self.hrefs:
            if node['id'] == href_id:
                return node
        raise Exception('There is no specific id:{} node in hrefs of node {}'.format(href_id, str(current_raw_node)))

    def get_children_titles_of_node(self, node):
        if "children" not in node and 'href' not in node:
            raise Exception('There is no child in {}'.format(
                self.get_title_from_xmind_node(node)))
        if 'href' in node:
            return [self.get_title_from_xmind_node(child) for child in self.get_children_nodes_from_xmind_node(node)]
        return [self.get_title_from_xmind_node(child) for child in self.get_children_nodes_from_xmind_node(node)]

    def check_node_status(self, node):
        pass
        # updated > saved > unsaved
        # node_status = NodeStatus.unsaved
        # if 'markers' not in node:
        #     pass
        # else:
        #     for marker in node['markers']:
        #         if marker['markerId'] == 'c_symbol_pen':
        #             node_status = NodeStatus.updated
        #         if marker['markerId'] == 'task-done':
        #             if node_status != NodeStatus.updated:
        #                 node_status = NodeStatus.saved
        # if 'href' in node:
        #     href_node = self.get_children_nodes_from_xmind_node(node)
        #     href_node_status = self.check_node_status(href_node)
        #     if href_node_status == NodeStatus.updated or node_status == NodeStatus.updated:
        #         node_status = NodeStatus.updated
        #     elif href_node == NodeStatus.saved or node_status == NodeStatus.saved:
        #         node_status = NodeStatus.saved
        #     else:
        #         node_status = NodeStatus.unsaved
        # return node_status

    def add_processed_marker(self, raw_node: Dict, hrefs):
        pass
        # # print(raw_node)
        # if 'href' in raw_node:
        #     href_node = get_href(raw_node, hrefs)
        #     add_processed_marker(href_node, hrefs)
        # if 'markers' not in raw_node:
        #     raw_node['markers']: List = [{'markerId': "task-done"}]
        # else:
        #     raw_node['markers']: List = list(filter(
        #         lambda marker: marker['markerId'] != 'c_symbol_pen' and marker['markerId'] != 'task-done',
        #         raw_node['markers']))
        #     raw_node['markers'].append({'markerId': "task-done"})

    def transform_xmind_node_to_processed_note(self, node, ancestors):
        return {'id': self.get_id_from_xmind_node(node),
                'title': self.get_title_from_xmind_node(node),
                'children': self.get_children_titles_of_node(node),
                'ancestors': ancestors}

    def parse_xmind(self):
        ancestor_list_stack = [[]]
        raw_node_stack = [self.root]
        parsed_nodes = []

        while len(raw_node_stack) != 0:
            node = raw_node_stack.pop()
            current_title = self.get_title_from_xmind_node(node)
            ancestors = ancestor_list_stack.pop()

            if "children" in node or 'href' in node:

                # print(1)
                # if check_node_status(node, hrefs) == NodeStatus.unsaved:
                #     print(2)
                #     add_processed_marker(node, hrefs)

                parsed_nodes.append(
                    self.transform_xmind_node_to_processed_note(node, ancestors))
                #     elif check_node_status(node, hrefs) is NodeStatus.saved:
                #         print(3)
                #         pass
                #     elif check_node_status(node, hrefs) is NodeStatus.updated:
                #         add_processed_marker(node, hrefs)
                #         print(4)
                #         processed_notes.append(
                #             {'node': trans_raw_node2processed_node(node, ancestors, hrefs),
                #              'status': NodeStatus.updated})
                children = self.get_children_nodes_from_xmind_node(node)
                raw_node_stack.extend(reversed(children))
                children_ancestors = ancestors.copy()
                children_ancestors.append(current_title)
                ancestor_list_stack.extend(
                    [children_ancestors for _ in range(len(children))])
            else:
                pass
            #     if check_node_status(node, hrefs) is NodeStatus.unsaved:
            #         add_processed_marker(node, hrefs)
            #     elif check_node_status(node, hrefs) is NodeStatus.saved:
            #         pass

        # print(xmind)
        return parsed_nodes
