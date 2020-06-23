import yara

class YaraRuleHandler(object):

    def __init__(self, file):
        self.file = file


    def test_compilation(self):
        try:
            rule = yara.compile(self.file)
            return True
        except :
            print("error")
            return False

