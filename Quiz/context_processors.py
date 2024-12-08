from django.contrib.auth.models import Group

def add_is_moderator(request):
    if request.user.is_authenticated:
        is_moderator = request.user.groups.filter(name='Moderator').exists()
    else:
        is_moderator = False
    return {'is_moderator': is_moderator}