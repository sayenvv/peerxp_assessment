from django import template

register = template.Library()

@register.filter
def get_current_user(session,*args):
    print(session,"sdsssssssss")
    return True