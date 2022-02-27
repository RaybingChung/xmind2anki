from tqdm import tqdm

import xmind_parser
from anki_connect import check_connection, add_note
from cvt2nt import cvt2ind_wri_nt_rem_path

# xmind = r'E:\MyLibrary\MyNote\托福作文\展开\品质类.xmind'
xmind_file_path = r'E:\MyLibrary\Hunt4job\找工 - Copy.xmind'

ordered_nodes, xmind = xmind_parser.traverse_nodes(xmind_file_path)
print(ordered_nodes)
xmind_parser.save_xmind(xmind_file_path, xmind)

if not check_connection():
    print("Anki not connect!!")
    exit(-1)
print('Anki connect.')

for node in tqdm(ordered_nodes):
    nt = cvt2ind_wri_nt_rem_path(node)
    add_note(nt)
