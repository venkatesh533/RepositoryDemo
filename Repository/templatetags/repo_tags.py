
from django import template
from Repository.models import *

register = template.Library()

@register.filter(is_safe=True)
def file_name(pk):
	obj = pk.split('/')[::-1][0]
	return obj