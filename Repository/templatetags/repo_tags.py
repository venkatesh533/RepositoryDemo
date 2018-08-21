
from django import template
from Repository.models import *
from DjangoProject.settings import MEDIA_ROOT

register = template.Library()

@register.filter(is_safe=True)
def file_name(pk):
	obj = pk.split('/')[::-1][0]
	return obj

@register.simple_tag
def getmedia_file(pk,file_type):
	obj = RepositoryFiles.objects.get(id=pk)
	if file_type == 'video':
		file_path = '/static/MediaFiles/' + obj.repo_video.name
	elif file_type == 'audio':
		file_path = '/static/MediaFiles/' + obj.repo_audio.name
	elif file_type == 'image':
		file_path = '/static/MediaFiles/' + obj.repo_image.name
	return file_path