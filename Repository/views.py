from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
import os

from Repository.models import *
from Repository.digg_paginator import *
# Create your views here.

## logout view ##
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

## home page ##
@login_required(login_url='/')
def dashboard(request):
	repos = Repository.objects.filter(active=2).order_by('-id')
	page = request.GET.get('page',1)
	count = 10
	s = range(0, repos.count())
	contacts = get_pagination(request,repos,count)
	return render(request,'crimedata/dashboard.html',locals())

## add repository page ##
@login_required(login_url='/')
def add_reposit(request):

	if request.method == 'POST':
		repo_id = request.POST.get('repo_id')
		repo_id = repo_id.strip()	
		if repo_id:
			rep_obj,created = Repository.objects.get_or_create(repo_id=repo_id)
			return HttpResponseRedirect('/repos-list/')
		else:
			error_msg = 'Please Enter Repository ID'

	return render(request,'crimedata/newrepo.html',locals())

## repositories list page ##
@login_required(login_url='/')
def repos_list(request):
	repos = Repository.objects.filter(active=2).order_by('-id')
	page = request.GET.get('page',1)
	count = 10
	s = range(0, repos.count())
	contacts = get_pagination(request,repos,count)
	# contacts_pagination = DiggPaginator(s, count, margin=1, tail=1, body=1).page(page)
	return render(request,'crimedata/repositorylist.html',locals())

## fun to upload file objects ##
def file_uploads(request,file_name):
	file_obj = ''
	try:
		file_obj = request.FILES[file_name]
	except MultiValueDictKeyError:
		file_obj = ''
	return file_obj

## repository detailed view ##
@login_required(login_url='/')
def repo_view(request,pk):
	data1 = page_redirection(request)
	repo_obj = Repository.objects.get(id=pk)
	repo_files = RepositoryFiles.objects.filter(active=2,repo=repo_obj).order_by('-id')
	page = request.GET.get('page',1)
	count = 5
	s = range(0, repo_files.count())
	contacts = get_pagination(request,repo_files,count)
	
	if request.method == 'POST':
		repo_files = RepositoryFiles.objects.filter(active=2,repo=repo_obj).order_by('-id')
		contacts = get_pagination(request,repo_files,count)
		## request file parameters ##
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

	return render(request,'crimedata/repository_view.html',locals())	

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

#### Pagination redirection view
def page_redirection(request):
    data1 = request.session.get('var3')
    
    if data1 == None or data1 == '':
        data1 = 1
    else:
        data1 = int(data1)
    return data1

## view to edit repository files ##
@login_required(login_url='/')
def edit_repofiles(request,pk):
	repofile_obj = RepositoryFiles.objects.get(id=pk)
	data1 = page_redirection(request)
	if request.method == 'POST':
		## request file parameters ##
		repo_image = file_uploads(request,'repo_image')
		repo_audio = file_uploads(request,'repo_audio')
		repo_video = file_uploads(request,'repo_video')
		
		if repo_image  :
			repofile_obj.repo_image = repo_image
		if repo_audio:
			repofile_obj.repo_audio = repo_audio
		if repo_video:
			repofile_obj.repo_video = repo_video
		repofile_obj.save()
		return HttpResponseRedirect('/repo-view/%d/?page=%d'%(repofile_obj.repo.id,data1))

	return render(request,'edit_repofiles.html',locals())

## To send otp to mobile number ##
def send_otp(request):

	if request.method == 'POST':
		mobile_no = request.POST.get('mobile_no')
		mobile_no = mobile_no.strip()
		user_obj = RepositoryUser.objects.get_or_none(mobile_no=mobile_no)
		if user_obj:
			from random import randint
			import requests
			otpno = randint(1000,9999)
			print(otpno)
			resp = requests.get('http://zebiapi.vizag.co/cdr1/148971/?mob_num={}&otp={}'.format(mobile_no,otpno))
			otp_obj,created = OTP.objects.get_or_create(repo_user=user_obj,otp_number=str(otpno))
			return HttpResponseRedirect('/verify-otp/{}'.format(user_obj.id))
		else:
			error_msg = 'Mobile no is not registered'
	return render(request,'crimedata/login.html',locals())

## To verify otp ##
def verify_otp(request,pk):
	user_obj = RepositoryUser.objects.get_or_none(id=pk)
	otp_obj = OTP.objects.get_or_none(repo_user=user_obj)
	status = False
	if request.method == 'POST':
		otp_no = request.POST.get('otp_no')
		otp_no = otp_no.strip()
		if otp_obj and otp_obj.otp_number == otp_no:
			status = True
			otp_obj.otp_verify = True
			otp_obj.save()
			if otp_obj.otp_verify:
				otp_obj.delete()
			login(request,user_obj.user)
			return HttpResponseRedirect('/verify-otp/{}/?msg=success'.format(user_obj.id))
		else:
			status = False
			error_msg = 'Invalid OTP'
		

	return render(request,'crimedata/verify_otp.html',locals())	
