"""DjangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Repository.views import *
from files_download import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('add-reposit/',add_reposit,name="add_reposit"),
    path('repos-list/',repos_list,name="repos_list"),
    path('repo-view/<int:pk>/',repo_view,name="repo_view"),
    path('download-file/<int:pk>/',download_file,name="download_file"),

]
