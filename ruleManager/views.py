from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadRuleForm
from .src.yaraRuleHandler import *
from .src.fileUploader import *
from .models import YaraRuleModel

# Create your views here.

def index(request):
    return render(request, 'ruleManager/index.html')


def upload_rule(request):
    if request.method == 'POST':
        form = UploadRuleForm(request.POST, request.FILES)
        file = FileUploader(request.FILES['file'],'./ruleManager/rules/'+request.FILES['file'].name)
        if form.is_valid():

            # Check if Yara Rule compile
            file.upload_file()
            yara = YaraRuleHandler(file.get_path())
            if yara.test_file() == False:
                if file.file_exist():
                    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'response': 'Yara Rule can\'t compile'})
                else:
                    file.delete_file()
                    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'response': 'Yara Rule can\'t compile'})
            else:
                if file.file_exist():
                    print("file exist, is remplaced")
                    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'response': 'file remplaced'})
                else:
                    saveToModel = YaraRuleModel(path =file.get_path())
                    print('saving')
                    saveToModel.save()
                    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'response': 'file uploaded'})
    else:
        form = UploadRuleForm()
    return render(request, 'ruleManager/uploadRule.html', {'form': form})