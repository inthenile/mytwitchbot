import os.path

class FileManager:
    """class to manage files easier within builds.py"""
    def __init__(self, filepath):
        self.filepath = filepath

    def file_create(self):
        """creates a file and then closes it"""
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w") as fl:
                fl.write("{}")
                fl.close()
        else:
            print("builds.json already exists.")

    def file_open_to_read(self):
        """opens a file, if it exists, to read it"""
        if os.path.exists(self.filepath):
            return open(self.filepath, "r")
        else:
            self.file_create()
    def file_open_to_write(self):
        """opens a file, if it exists, to write to it"""
        if os.path.exists(self.filepath):
            return open(self.filepath, "w")
        else:
            print("file does not exist")

    def file_close(self, fileobject):
        """if the given file exists, closes it."""
        if os.path.exists(self.filepath):
            try:
                fileobject.close()
            except AttributeError:
                print("Make sure the parameter is a file object!")
        else:
            print("file does not exist")

filemanager = FileManager("gw2builds/builds.json")
# ensuring that the file should always exist at the start of the program.
filemanager.file_create()

