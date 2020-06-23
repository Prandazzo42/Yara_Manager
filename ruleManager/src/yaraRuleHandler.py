import yara
from ..models import *

"""
Class YaraRuleHandler(filePath)

filePath <String> : path to the file

Class to check if file is with yara
"""
class YaraRuleHandler(object):

    def __init__(self, filePath):
        self.file = filePath

    # Try to compile the given file
    #
    # return Boolean
    def test_compilation(self):
        try:
            rule = yara.compile(self.file)
            return True
        except :
            return False

    # try to compile an other file
    # if success, return yara.Rules
    # else, return False
    def compile_file(filePath):
        try:
            return yara.compile(filePath)
        except :
            return False 
