from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db import models

User = get_user_model()


class Conversation(models.Model):
    member = models.ManyToManyField(Session, blank=True)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    author = models.ForeignKey(Session, related_name='author_messages', on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.author.session_key + ' : ' + self.content
