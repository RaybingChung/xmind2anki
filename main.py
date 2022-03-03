from xmind2anki import Courier

if __name__ == '__main__':
    xmind_file_path: str = r'E:\MyLibrary\Hunt4job\找工altered - Copy.xmind'

    transformer = Courier(xmind_file_path)

    transformer.set_note_type('tif')
    print('Successfully transform xmind note to anki note.')
