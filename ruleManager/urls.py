from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploadRule/', views.upload_rule, name='upload_rule'),

    path('editTag/', views.edit_tag, name='edit_tag'),
    path('editTag/<int:tagId>', views.delete_tag, name='delete_tag'),

    path('getRules/', views.get_rules, name='get_rules'),
    path('getRules/edit/<int:ruleId>', views.edit_rule, name='edit_rule'),
    path('getRules/delete/<int:ruleId>', views.delete_rule, name='delete_rule'),
    path('getRules/export/<int:ruleId>', views.export_rule, name='export_rule'),

    path('testFile/', views.test_file, name='test_file'),
]