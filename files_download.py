from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.utils.encoding import smart_str
import os
from wsgiref.util import FileWrapper
import os, tempfile, zipfile
import mimetypes

from Repository.models import *

def download_file(request,pk):
    file_type = request.GET.get('file_type')
    try :
        obj = RepositoryFiles.objects.get(id=pk)
        if file_type == 'image':
            download_file = obj.repo_image
        elif file_type == 'audio':
            download_file = obj.repo_audio
        elif file_type == 'video':
            download_file = obj.repo_video
        elif file_type == 'document':
            download_file = obj.repo_document
    except :
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    file_name = str(download_file.name)
    file_path = settings.MEDIA_ROOT+file_name
    
    content_type = mimetypes.guess_type(file_name.split('/')[::-1][0])[0]
    wrapper = FileWrapper(open(file_path,'rb'))
    response = HttpResponse(wrapper,content_type=content_type)
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = 'attachment; filename=%s' %(file_name.split('/')[::-1][0])

    return response

