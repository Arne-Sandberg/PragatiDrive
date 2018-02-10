from django import template

register = template.Library()

@register.filter(name='DynamicIndexAccess')

def DynamicIndexAccess(array, index):
	return array[index]