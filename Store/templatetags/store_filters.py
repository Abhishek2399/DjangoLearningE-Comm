from django import template

register = template.Library()

@register.filter
def get_val(obj, key):
    return obj.get(key.lower(), f"Key:'{key}' not found in Dict:{obj}")
    
