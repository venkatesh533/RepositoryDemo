from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os

from Repository.models import *
from Repository.digg_paginator import *
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
	repos = Repository.objects.filter(active=2).order_by('-id')
	page = request.GET.get('page',1)
	count = 10
	s = range(0, repos.count())
	contacts = get_pagination(request,repos,count)
	# contacts_pagination = DiggPaginator(s, count, margin=1, tail=1, body=1).page(page)
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
	page = request.GET.get('page',1)
	count = 5
	s = range(0, repo_files.count())
	contacts = get_pagination(request,repo_files,count)
	if request.method == 'POST':
		repo_image = file_uploads(request,'repo_image')
		repo_audio = file_uploads(request,'repo_audio')
		repo_video = file_uploads(request,'repo_video')
		
		if repo_image or repo_audio or repo_video:
			repofile_obj = RepositoryFiles.objects.create(repo=repo_obj)
			repofile_obj.repo_image = repo_image
			repofile_obj.repo_audio = repo_audio
			repofile_obj.repo_video = repo_video
			repofile_obj.save()
		else:
			msg = 'Please upload atleast one image/audio/video file'

	return render(request,'repo_view.html',locals())	

#### pagination for the listing pages
def get_pagination(request, plist, count):                                       					
    # Pagination Function
    # return a page number with the list of items
    paginator = Paginator(plist, count)
    page = request.GET.get('page', '')
    try:
        plist = paginator.page(page)
    except PageNotAnInteger:
       # If page is not an integer, deliver first page.
        plist = paginator.page(1)
    except EmptyPage:
       # If page is out of range (e.g. 9999), deliver last page of results.
        plist = paginator.page(paginator.num_pages)
    request.session['var3'] = page
    return plist


