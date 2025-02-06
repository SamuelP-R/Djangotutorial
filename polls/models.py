import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User



# Primer  Modelo
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    creared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_questions", default=1), # id del admin
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.question_text
    @admin.display(
        boolean=True,
        ordering="pub_date",
        description="Published recently?",
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    


class Choice(models.Model):
    question = models.ForeignKey(Question,
on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text 
    

# Modelo para registrar quien ya ha votado
class Voted(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    vote_date = models.DateTimeField(auto_now_add=True)
    #Solo un usuario puede votar una pregunta 
    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f'{self.user} voto en "{self.question}" por "{self.choice}"'
    