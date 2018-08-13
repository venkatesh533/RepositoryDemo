from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError

from Repository.models import *
# Create your views here.

## home page ##
def home(request):
	return render(request,'home.html',locals())

## add repository page ##
def add_reposit(request):

	if request.method == 'POST':
		repo_id = request.POST.get('repo_id')
		if repo_id:
			rep_obj,created = Repository.objects.get_or_create(repo_id=repo_id)
			return HttpResponseRedirect('/repos-list/')
		else:
			error_msg = 'Please Enter Repository ID'

	return render(request,'add_reposit.html',locals())

## repositories list page ##
def repos_list(request):
	repos = Repository.objects.filter(active=2)
	return render(request,'repos_list.html',locals())

## fun to upload file objects ##
def file_uploads(request,file_name):
	file_obj = ''
	try:
		file_obj = request.FILES[file_name]
	except MultiValueDictKeyError:
		file_obj = ''
	return file_obj

## repository detailed view ##
def repo_view(request,pk):
	repo_obj = Repository.objects.get(id=pk)
	repo_files = RepositoryFiles.objects.filter(active=2,repo=repo_obj).order_by('-id')
	if request.method == 'POST':
		repo_image = file_uploads(request,'repo_image')
		repo_audio = file_uploads(request,'repo_audio')
		repo_video = file_uploads(request,'repo_video')
		repofile_obj = RepositoryFiles.objects.create(repo=repo_obj)
		repofile_obj.repo_image = repo_image
		repofile_obj.repo_audio = repo_audio
		repofile_obj.repo_video = repo_video
		repofile_obj.save()


	return render(request,'repo_view.html',locals())	





