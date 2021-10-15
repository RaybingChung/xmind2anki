# Xmind2Anki
This cods implements a simple tool to convert XMind files to Anki cards. Initially, I devise an idea to assist myself in memorizing some writing sample since I have struggled for months to cope with the TOEFL writing test. XMind helps me to parse others' writing samples, and Anki helps me memorize something. However, both of them have drawbacks. It is true that XMind organizes knowledge points well, but most of time I seldom or even am relunctant to look back on them, leading to less remembering. As for anki, indeed, it simplifies the process to memorize things for me, but it will leave the knowledge points in a mess, just as learning by rotes to some extent. Therefore, I make my attempt to combine these two tools together hoping that I can give full play to them and obatin worthwhile grades.

## Introduction
This tool can transfer every node in XMind trees into anki cards. For the sake of swift development, some common functions already existed in anki is avoided. In other word, you need to do some adjustments in anki to apply this code. __You need to new a model named__ _SkeletionMemorizing_ __with three fields named__ _Id, Node, Children and Anchestors_ __and make card templates respectively__. __Watch out that you should let__ _Id_ __to be the first field in Anki in case of adding notes that have identical fields__. Then feel free to do the transfer by altering and runing the _xmind_parse.py_ file. It is true that this code has a graphical interface, but it is too ugly owing to my poor development capacity and the rigidity of PYQT5. Thus, I don't recommend using the graphical interface (LOL).

### Operative Environment
Anki Add-on: Follow the guide in [AnkiConnect](https://github.com/FooSoft/anki-connect) and install the extension in Anki named AnkiConnect which is the prerequisite of this code.  
Language: python > 3.6  
Operation System: Since the codes are developed in Win10, it would be better to run them in Windows environment.  
Third Packages: The 3rd party packages in this code are very common. In order to run the code, you need to install them.  

### Acknowledgement
Special thanks to [AnkiConnect](https://github.com/FooSoft/anki-connect). They are the indispensible parts for me to implement the codes.

## Lisence
GPL