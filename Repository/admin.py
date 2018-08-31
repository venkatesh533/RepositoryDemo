from django.contrib import admin
from Repository.models import *

# Register your models here.
admin.site.register(Repository)
admin.site.register(RepositoryFiles)
admin.site.register(RepositoryUser)
admin.site.register(OTP)