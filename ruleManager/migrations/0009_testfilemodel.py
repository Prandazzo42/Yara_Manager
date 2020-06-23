# Generated by Django 3.0.7 on 2020-06-23 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ruleManager', '0008_yararulemodel_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestFileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.FilePathField(path='./ruleManager/testFiles/')),
                ('name', models.CharField(default=None, max_length=256)),
            ],
        ),
    ]
