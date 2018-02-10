from django import template

register = template.Library()

@register.filter(name='dynamicindexaccess')


def dynamicindexaccess(array, index):
	return array[index]