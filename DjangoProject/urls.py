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
    path('dashboard/',dashboard,name="dashboard"),
    path('add-reposit/',add_reposit,name="add_reposit"),
    path('repos-list/',repos_list,name="repos_list"),
    path('repo-view/<int:pk>/',repo_view,name="repo_view"),
    path('edit-repofiles/<int:pk>/',edit_repofiles,name="edit_repofiles"),
    path('download-file/<int:pk>/',download_file,name="download_file"),
    path('',send_otp,name="send_otp"),
    path('verify-otp/<int:pk>/',verify_otp,name="verify_otp"),
    path('logout/',logout_view,name="logout_view"),

]
