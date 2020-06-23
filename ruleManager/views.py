from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .src.yaraRuleHandler import *
from .src.fileUploader import *
from .models import *
import mimetypes, os, time

# url: '/'
def index(request):
    rules = YaraRuleModel.objects.all()
    tags = TagModel.objects.all()
    return render(request, 'ruleManager/index.html', {'rules': rules, 'tags': tags})

# url: '/uploadRule/'
def upload_rule(request):
    tags = TagModel.objects.all()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = FileUploader(request.FILES['file'],'./ruleManager/rules/'+request.FILES['file'].name)
        if form.is_valid():
            file.upload_file()

            # Check if Yara Rule compile
            yara = YaraRuleHandler(file.get_path())
            if yara.test_compilation() == False:
                if file.file_exist() == False:
                    file.delete_file()
                return render(request, 'ruleManager/uploadRule.html', {'form': form, 'tags': tags, 'response': 'Rules can\'t compile'})
            
            else:
                if file.file_exist():
                    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'tags': tags, 'response': 'file is overwritten'})
                else:
                    try:
                        # Save in Database Rules file
                        saveToModel = YaraRuleModel(path =file.get_path(), name = file.get_name())
                        saveToModel.save()

                        # Save in Database Tags for the given rules
                        tagArray = request.POST.copy()
                        for tag in tagArray.pop('tag'):
                            ruleTagInstance = RulesTagsModel(rule = saveToModel, tag = TagModel.objects.get(id = tag))
                            ruleTagInstance.save()
                        return render(request, 'ruleManager/uploadRule.html', {'form': form,'tags': tags, 'response': 'file is uploaded'})
                    except Exception as e:
                        file.delete_file()
                        return render(request, 'ruleManager/uploadRule.html', {'form': form,'tags': tags, 'response': e})
    else:
        form = UploadFileForm()
    return render(request, 'ruleManager/uploadRule.html', {'form': form, 'tags': tags})

# url: '/editTag/'
def edit_tag(request):
    tags = TagModel.objects.all()

    if request.method == 'POST':
        form = CreateTag(request.POST)
        if form.is_valid():
            try:
                # Save in Database new Tag
                saveTag = TagModel(tag = request.POST['newTag'])
                saveTag.save()
                return render(request, 'ruleManager/editTag.html', {'form': form, 'response': 'Tag has been Created', 'tags': tags})
            except Exception as e:
                return render(request, 'ruleManager/editTag.html', {'form': form, 'response': e, 'tags': tags})
        else:
            return render(request, 'ruleManager/editTag.html', {'form': form, 'response': 'Error has occurred', 'tags': tags})
    else:
        form = CreateTag()
        return render(request, 'ruleManager/editTag.html', {'form': form, 'tags': tags})

# url: '/editTag/<Int:tagId>/'
def delete_tag(request, tagId):
    tagToRemove = TagModel.objects.filter(id = tagId)
    try:
        tagToRemove.delete()   
    except Exception as e:
        print(e)
    finally:
        return redirect('/editTag/')

# url: '/getRules/'
def get_rules(request):
    rules = YaraRuleModel.objects.all()
    tags = TagModel.objects.all()
    ruleTags = RulesTagsModel.objects.all()
    return render(request, 'ruleManager/getRules.html', {'rules': rules, 'tags': tags, 'ruleTags':ruleTags})

# url: 'getRules/edit/<int:ruleId>'
def edit_rule(request, ruleId):
    if request.method == 'POST':
        ruleTags = RulesTagsModel.objects.filter(rule = ruleId)
        try:
            ruleTags.delete()
            tagArray = request.POST.copy()
            try:
                for tag in tagArray.pop('tag'):
                    ruleTagInstance = RulesTagsModel(rule = YaraRuleModel.objects.get(id = ruleId), tag = TagModel.objects.get(id = tag))
                    ruleTagInstance.save()
                
            except Exception as errorSave:
                print(errorSave)
            finally:
                return redirect('/getRules/')
        except Exception as errorDel:
            print(errorDel)
        finally:
            return redirect('/getRules/')
    else:
        rule = YaraRuleModel.objects.get(id = ruleId)
        tags = TagModel.objects.all()
        ruleTags = RulesTagsModel.objects.filter(rule = ruleId)
        return render(request, 'ruleManager/editRule.html', {'rule': rule, 'tags': tags, 'ruleTags': ruleTags })

# url: 'getRules/delete/<int:ruleId>'
def delete_rule(request, ruleId):
    ruleFile = YaraRuleModel.objects.get(id = ruleId)
    try:
        os.unlink(path=ruleFile.path)
        rule = YaraRuleModel.objects.filter(id = ruleId)
        rule.delete()
    except Exception as e:
        print(e)
    finally:
        return redirect('/getRules/')

# url: 'getRules/export/<int:ruleId>'
def export_rule(request, ruleId):
    rule = YaraRuleModel.objects.get(id = ruleId)
    filePath = rule.path
    filename = rule.name

    file = open(filePath, 'r')
    mime_type = mimetypes.guess_type(filePath)
    response = HttpResponse(file, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response


# url: '/testFile/'
def test_file(request):
    tags = TagModel.objects.all()

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        file = FileUploader(request.FILES['file'],'./ruleManager/testFiles/'+request.FILES['file'].name)
        if form.is_valid():
            try:
                file.upload_file()


                rulesSet = set([])
                matchingRules = dict()

                # start Timer
                startTime = time.time()
                if request.POST.__contains__('tag'):
                    tagArray = request.POST.copy().pop('tag')
                    for tag in tagArray:
                        # get RulesTag for given tag id
                        for rulesTags in RulesTagsModel.objects.filter(tag_id = tag):
                            rule = YaraRuleModel.objects.get(id = rulesTags.rule_id)

                            # check if name is in ruleSet, 
                            # if not, add it to ruleSet then compile yaraRule from file thanks to the path
                            if rule.name not in rulesSet:
                                rulesSet.add(rule.name)
                                ruleYara = YaraRuleHandler.compile_file(filePath = rule.path)
                                
                                # Check if a compiled rule match with given file,
                                # add result to matchingRules
                                match = ruleYara.match(filepath = file.get_path())
                                matchingRules[rule.name] = match
                            else:
                                pass
                else:
                    # get all RulesTag
                    for rulesTags in RulesTagsModel.objects.all():
                        rule = YaraRuleModel.objects.get(id = rulesTags.rule_id)
                        
                        # check if name is in ruleSet, 
                        # if not, add it to ruleSet then compile yaraRule from file thanks to the path
                        if rule.name not in rulesSet:
                            rulesSet.add(rule.name)
                            ruleYara = YaraRuleHandler.compile_file(filePath = rule.path)
                            
                            # Check if a compiled rule match with given file,
                            # add result to matchingRules
                            match = ruleYara.match(filepath = file.get_path())
                            matchingRules[rule.name] = match
                        else:
                            pass
                endTime = time.time()
                duration = endTime - startTime
                file.delete_file()
                return render(request, 'ruleManager/testFile.html', {'form': form,'tags': tags, 'response': 'file has been tested', 'result': {'matchingRules':matchingRules,'duration': duration, "success":True}})
            except Exception as e:
                return render(request, 'ruleManager/testFile.html', {'form': form,'tags': tags, 'response': e})
    else:
        form = UploadFileForm()
    return render(request, 'ruleManager/testFile.html', {'form': form, 'tags': tags})