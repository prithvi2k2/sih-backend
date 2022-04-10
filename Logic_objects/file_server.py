import config
from web3 import Web3
import os
import uuid
from flask import current_app


class File_server(object):
    def __init__(self, file_type) -> None:

        if file_type == "audio":
            self.folder = "audio"
        elif file_type == "image":
            self.folder = "image"
        elif file_type == "video":
            self.folder = "video"
        else:
            self.folder = None

    def save_file(self, file):
        if not self.folder:
            return
        self.file = file
        self.file_extension = file.filename.rsplit('.', 1)[1]
        filename = str(uuid.uuid4()) + "." + self.file_extension
        self.filename = filename

        path = str(os.getcwd() + f"/FILES/{self.folder}/")
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
        self.file.save(os.path.join(path, filename))
        print(type(filename))
        return str(filename)


# test = file_server("audio" , 1)
