from xmind2anki import Courier

if __name__ == '__main__':
    xmind_file_path: str = r'E:\MyLibrary\XmindRepo\后端开发面试知识.xmind'

    courier = Courier(xmind_file_path)

    courier.set_note_type('jik')

    courier.upload_all_changes_to_anki()
    print('Successfully transform xmind note to anki note.')

