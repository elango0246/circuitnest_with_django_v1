from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='home'), path('contact/', views.contact, name='contact'), path('api/projects/', views.project_api, name='project_api')]