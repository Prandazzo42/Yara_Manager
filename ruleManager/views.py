from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .src.yaraRuleHandler import *
from .src.fileUploader import *
from .models import *
import mimetypes, os

# Create your views here.

def index(request):
    return render(request, 'ruleManager/index.html')


def upload_rule(request):
    tags = TagModel.objects.all()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = FileUploader(request.FILES['file'],'./ruleManager/rules/'+request.FILES['file'].name)
        if form.is_valid():

            # Check if Yara Rule compile
            file.upload_file()
            yara = YaraRuleHandler(file.get_path())
            if yara.test_compilation() == False:
                if file.file_exist() == False:
                    file.delete_file()
                return render(request, 'ruleManager/uploadRule.html', {'form': form, 'tags': tags, 'response': 'Yara Rule can\'t compile'})
            else:
                if file.file_exist():
                    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'tags': tags, 'response': 'file remplaced'})
                else:
                    saveToModel = YaraRuleModel(path =file.get_path(), name = file.get_name())
                    saveToModel.save()
                    tagArray = request.POST.copy()
                    print(tagArray)
                    for tag in tagArray.pop('tag'):
                        ruleTagInstance = RulesTagsModel(rule = saveToModel, tag = TagModel.objects.get(id = tag))
                        ruleTagInstance.save()
                    return render(request, 'ruleManager/uploadRule.html', {'form': form,'tags': tags, 'response': 'file uploaded'})
    else:
        form = UploadFileForm()
    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'tags': tags})


def edit_tag(request):
    tags = TagModel.objects.all()
    if request.method == 'POST':
        form = CreateTag(request.POST)
        if form.is_valid():
            try:
                saveTag = TagModel(tag = request.POST['newTag'])
                saveTag.save()
                return render(request, 'ruleManager/editTag.html', {'form': form, 'response': 'Tag Created', 'tags': tags})
            except:
                return render(request, 'ruleManager/editTag.html', {'form': form, 'response': 'Error', 'tags': tags})
        else:
            return render(request, 'ruleManager/editTag.html', {'form': form, 'response': 'Error', 'tags': tags})
    else:
        form = CreateTag()
        return render(request, 'ruleManager/editTag.html', {'form': form, 'tags': tags})

def delete_tag(request, tagId):
    tagToRemove = TagModel.objects.filter(id = tagId)
    tagToRemove.delete()

    return redirect('/editTag/')


def get_rules(request):
    rules = YaraRuleModel.objects.all()
    tags = TagModel.objects.all()
    ruleTags = RulesTagsModel.objects.all()
    return render(request, 'ruleManager/getRules.html', {'rules': rules, 'tags': tags, 'ruleTags':ruleTags})

def edit_rule(request, ruleId):
    if request.method == 'POST':
        ruleTags = RulesTagsModel.objects.filter(rule = ruleId)
        ruleTags.delete()
        tagArray = request.POST.copy()
        for tag in tagArray.pop('tag'):
            ruleTagInstance = RulesTagsModel(rule = YaraRuleModel.objects.get(id = ruleId), tag = TagModel.objects.get(id = tag))
            ruleTagInstance.save()
        return redirect('/getRules/')
    else:
        rule = YaraRuleModel.objects.get(id = ruleId)
        tags = TagModel.objects.all()
        ruleTags = RulesTagsModel.objects.filter(rule = ruleId)
        return render(request, 'ruleManager/editRule.html', {'rule': rule, 'tags': tags, 'ruleTags': ruleTags })

def delete_rule(request, ruleId):
    ruleFile = YaraRuleModel.objects.get(id = ruleId)
    os.unlink(path=ruleFile.path)

    rule = YaraRuleModel.objects.filter(id = ruleId)
    rule.delete()
    return redirect('/getRules/')

def export_rule(request, ruleId):
    rule = YaraRuleModel.objects.get(id = ruleId)
    fl_path = rule.path
    filename = rule.name

    fl = open(fl_path, 'r')
    mime_type = mimetypes.guess_type(fl_path)
    response = HttpResponse(fl, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response



def test_file(request):
    tags = TagModel.objects.all()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = FileUploader(request.FILES['file'],'./ruleManager/testFiles/'+request.FILES['file'].name)
        if form.is_valid():
            saveToModel = TestFileModel(path =file.get_path(), name = file.get_name())
            saveToModel.save()
            tagArray = request.POST.copy()
            if tagArray.pop('tag') != None:
                for in RulesTagsModel.objects.filter(tag_id in tagArray.pop('tag'))
            return render(request, 'ruleManager/uploadRule.html', {'form': form,'tags': tags, 'response': 'file uploaded'})
    else:
        form = UploadFileForm()
    return render(request, 'ruleManager/testFile.html', {'form': form, 'tags': tags})