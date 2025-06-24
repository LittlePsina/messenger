# chat/models.py
from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)  # Флаг группового чата
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} in {self.chat}'