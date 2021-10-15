import sys
from copy import deepcopy

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from main_window import Ui_MainWindow
from anki_connect import AnkiConnector
from xmind_parser import XMindParser

anki_connector = AnkiConnector()



class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
        self.connect_anki()
        self.selected_XMind_file = None
        self.selected_deck = "Default"
        self.selected_model = "SkeletonMemorizing"
        self.ok_label.setVisible(False)

    def connect_anki(self):
        if not anki_connector.check_connection():
            self.connect_again.setVisible(True)
            self.anki_connection.setVisible(True)
            self.transfer_button.setEnabled(False)
        else:
            # self.connect_again.setEnabled(False)
            self.connect_again.setVisible(False)
            self.anki_connection.setVisible(False)
            self.transfer_button.setEnabled(True)
            deck_names = anki_connector.get_deck_name()
            self.comboBox.addItems(deck_names)

    def button_clicked(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileUrl(self, options=options)
        self.current_file_name_box.setText(file_name.path()[1:])
        self.selected_XMind_file = file_name.path()[1:]
        # print(file_name.path())

    def create_new_deck(self):
        pass

    def transfer_notes_to_anki(self):
        xmind_parser = XMindParser(self.selected_XMind_file)
        xmind_parser.traverse()
        anki_connector.unsent_notes = deepcopy(xmind_parser.unstashed_nodes)
        xmind_parser.flush_nodes()
        anki_connector.deck_name = self.selected_deck
        anki_connector.model_name = self.selected_model
        anki_connector.add_notes()
        self.ok_label.setVisible(True)

    def select_deck(self):
        self.selected_deck = self.comboBox.currentText()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    myWin = MyMainForm()

    myWin.show()

    sys.exit(app.exec_())
