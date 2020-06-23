import os
from ..models import *


"""
Class FileUploader(file, nameFile)

file <File Objectts> 
name <string> : path to the file

Manage file on the server
"""
class FileUploader(object):

    def __init__(self, file, nameFile):
        self.file = file,
        self.nameFile = nameFile

    # Upload file to the given path
    #
    # return Boolean
    def upload_file(self):
        try:
            with open(self.nameFile, 'wb+') as rule:
                for chunk in self.file[0].chunks():
                    rule.write(chunk)
            return True
        except Exception as e:
            print(e)
            return False

    # Check if file exist in Database
    #
    # return Boolean
    def file_exist(self):
        if self.get_file_from_bdd():
            return True
        else:
            return False

    # return String
    def get_path(self):
        return self.nameFile

    # return String
    def get_name(self):
        return self.nameFile.split("/")[-1]

    # Delete file from given path
    #
    # return Boolean
    def delete_file(self):
        try:
            os.unlink(self.nameFile)
            return True
        except Exception as e:
            return False

    # Try to get YaraRuleModel object from database with given path
    #
    # if exist, return YaraRuleModel Object
    # else, return False
    def get_file_from_bdd(self):
        try:
            return YaraRuleModel.objects.filter(path = self.nameFile)
        except:
            return False