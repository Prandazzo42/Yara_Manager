from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('uploadRule/', views.upload_rule, name='upload_rule')
]