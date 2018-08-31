from django.db import models 
## Model managers for changemaker app models ##

class CustomQuerySet(models.QuerySet):

	def active_items(self):
		## returns active items only ##
		return self.filter(active=2)

	def get_or_none(self, *args, **kwargs):
		## whether object is existed or not
		try:
			return self.get(*args,**kwargs)
		except self.model.DoesNotExist:
			return None

	def ids(self):
		## returns the list of object ids ##
		return [i.id for i in self]

	def get_alivecms(self):
		return self.filter(soft_delete='SH')