from django.db import models
from django.contrib.auth.models import User
from Repository.manager import CustomQuerySet

# Create your models here.

ACTIVE_CHOICES = ((0, 'Inactive'), (2, 'Active'),)
class BaseContent(models.Model):
    active = models.PositiveIntegerField(choices=ACTIVE_CHOICES,default=2)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    modified = models.DateTimeField(auto_now=True,null=True,blank=True)
    ## custom queryset is the model manager ##
    objects = CustomQuerySet.as_manager()

## model to create repositories ##
class Repository(BaseContent):
	repo_id = models.CharField(max_length=8000,null=True,blank=True)
	name = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return str(self.repo_id)

## To save image/audio/video files ##
class RepositoryFiles(BaseContent):
	repo = models.ForeignKey(Repository,on_delete=models.CASCADE,null=True,blank=True)
	repo_image = models.ImageField(upload_to='Images/%Y/%m/%d',null=True,blank=True)
	repo_audio = models.FileField(upload_to='Audios/%Y/%m/%d',null=True,blank=True)
	repo_video = models.FileField(upload_to='Videos/%Y/%m/%d',null=True,blank=True)
	repo_document = models.FileField(upload_to='Documents/%Y/%m/%d',null=True,blank=True)
	
	def __str__(self):
		return str(self.repo.repo_id)	


## Model to register the users with mobile no in site ##
class RepositoryUser(BaseContent):
	user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
	mobile_no = models.CharField(max_length=250,null=True,blank=True)

	def __str__(self):
		return str(self.mobile_no)

## Model to send otp to users ##
class OTP(BaseContent):
	repo_user = models.ForeignKey(RepositoryUser,on_delete=models.CASCADE,null=True,blank=True)
	otp_number = models.CharField(max_length=250,null=True,blank=True)
	otp_verify = models.BooleanField(default=False,blank=True)

	def __str__(self):
		return str(self.repo_user.mobile_no)

