import os
from ..models import *

class FileUploader(object):

    def __init__(self, file, nameFile):
        self.file = file,
        self.nameFile = nameFile

    def upload_file(self):
        with open(self.nameFile, 'wb+') as rule:
            print(self.file)
            for chunk in self.file[0].chunks():
                rule.write(chunk)

    def file_exist(self):
        if self.get_file_from_bdd():
            return True
        else:
            return False

    def get_path(self):
        return self.nameFile

    def delete_file(self):
        os.unlink(self.nameFile)

    def get_file_from_bdd(self):
        try:
            return YaraRuleModel.objects.filter(path = self.nameFile)
        except:
            return False