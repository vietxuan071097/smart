# manager/views.py
import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.shortcuts import render

from chat.models import Conversation

@login_required
def index(request):
    if not request.session.session_key:
        request.session.save()

    session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)
    conversations = Conversation.objects.filter(member__in=[session])
    if request.user.id != 1:
        if conversations.count() < 1:
            cs = Conversation.objects.create()
            cs.member.add(session)
        else:
            cs = conversations[0]
        for ss in Session.objects.all():
            session_data = ss.get_decoded()
            if session_data != {}:
                uid = session_data.get('_auth_user_id')
                if uid == '1' and ss not in cs.member.all():
                    cs.member.add(ss)

    print(session.get_decoded(), session_key)

    return render(request, 'chat/chat.html', {
        'user_name': request.user,
        'SID': request.session.session_key,
        'conversations': conversations
    })
