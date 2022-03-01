from tqdm import tqdm

from anki_connect import check_connection, add_note, update_note
from node2note import cvt2toefl_independent_writing_note
from xmind_parser import XmindParser

xmind_file_path: str = r'E:\MyLibrary\Hunt4job\找工altered - Copy.xmind'


class Transformer:
    xmind_parser = XmindParser(xmind_file_path)
    print(xmind_parser.parsed_notes)


# xmind = r'E:\MyLibrary\MyNote\托福作文\展开\品质类.xmind'


# ordered_nodes_and_status, xmind = xmind_parser.parse_xmind(xmind_file_path)
# print(ordered_nodes_and_status)
# xmind_parser.save_xmind(xmind_file_path, xmind)
# if not check_connection():
#     print("Anki not connect!!")
#     exit(-1)
# print('Anki connect.')
#
# for node_and_status in tqdm(ordered_nodes_and_status):
#     nt = cvt2toefl_independent_writing_note(node_and_status['node'])
#     if node_and_status['status'] == xmind_parser.NodeStatus.unsaved:
#         add_note(nt)
#         continue
#     elif node_and_status['status'] == xmind_parser.NodeStatus.updated:
#         print(nt)
#         update_note(nt)
#         continue
#     else:
#         raise Exception('Unresolved Node Status.')
