from django.db import models

# Create your models here.

class YaraRuleModel(models.Model):
    path = models.FilePathField(path='./ruleManager/rules/')

    def __unicode__(self):
        return "{0} ".format(self.path)