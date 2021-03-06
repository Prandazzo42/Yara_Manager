# Generated by Django 3.0.7 on 2020-06-21 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ruleManager', '0004_auto_20200621_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=128, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RulesTagsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ruleManager.YaraRuleModel')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ruleManager.TagModel')),
            ],
        ),
    ]
