import xmind_parser
from anki_connect import check_connection, add_note
from cvt2nt import cvt2ind_wri_nt

xmind = r''

ordered_nodes = xmind_parser.traverse_nodes(xmind)

if not check_connection():
    print("Anki not connect!!")
    exit(-1)

for node in ordered_nodes:
    nt = cvt2ind_wri_nt(node)
    add_note(nt)
