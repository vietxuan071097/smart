from django import template
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session

register = template.Library()


@register.simple_tag
def get_companion(conversation, session_key):
    try:
        ss = Session.objects.get(session_key=session_key)
        uid = ss.get_decoded()['_auth_user_id']
        if uid == '1':
            return "Guess"
    except:
        pass

    for ss in conversation.member.all():
        if ss.session_key != session_key:
            try:
                uid = ss.get_decoded()['_auth_user_id']
                user = User.objects.get(id=uid)
                return user.username
            except:
                pass
    return "Guess"
