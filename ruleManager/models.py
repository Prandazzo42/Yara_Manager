from django.db import models

# Create your models here.

class YaraRuleModel(models.Model):
    path = models.FilePathField(path='./ruleManager/rules/')
    name = models.CharField(max_length=256, default=None)

    def __unicode__(self):
        return "{0} ".format(self.path)

class TagModel(models.Model):
    tag = models.CharField(max_length=128, unique=True)

class RulesTagsModel(models.Model):
    rule = models.ForeignKey(YaraRuleModel, on_delete=models.CASCADE)
    tag = models.ForeignKey(TagModel, on_delete=models.CASCADE)

class TestFileModel(models.Model):
    path = models.FilePathField(path='./ruleManager/testFiles/')
    name = models.CharField(max_length=256, default=None)