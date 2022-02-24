import xmind_parser
from anki_connect import check_connection, add_note
from cvt2nt import cvt2ind_wri_nt_rem_path
from tqdm import tqdm

xmind = r'E:\MyLibrary\MyNote\托福作文\展开\工作类.xmind'

ordered_nodes = xmind_parser.traverse_nodes_rem_path(xmind)

if not check_connection():
    print("Anki not connect!!")
    exit(-1)
print('Anki connect.')

for node in tqdm(ordered_nodes):
    # nt = cvt2ind_wri_nt(node)
    nt = cvt2ind_wri_nt_rem_path(node)
    add_note(nt)
