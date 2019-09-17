from django import template

register = template.Library()


@register.filter(name="étoile")
def étoile(value):
    return value.replace("*", "/")

@register.filter(name="to1")
def space(value):
    return value.replace("-", "'")
@register.filter(name='to')
def to(value):
    return value.replace("_"," ")

@register.filter(name="res")
def res(value):
    return value.replace(value,"res")