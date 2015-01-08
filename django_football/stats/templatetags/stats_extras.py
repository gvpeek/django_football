from django import template

register = template.Library()

@register.filter
def getitem(item, string):
  return getattr(item,string)