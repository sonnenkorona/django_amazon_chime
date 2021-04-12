from django import template

register = template.Library()

@register.filter
def replace1(value):
    return str(value["Meeting"]).replace("'",'"')

@register.filter
def replace2(value):
    if value == "":
        return ""
    else:
        return str(value["Attendee"]).replace("'",'"')
