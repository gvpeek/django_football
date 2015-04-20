from django import template

register = template.Library()

@register.filter
def dictget(dictionary, key):
    """
    Gets the value from the given dictionary for the given key and returns an empty string 
    if the key is not found.
    """
    return dictionary.get(key, '')