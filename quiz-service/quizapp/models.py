from django.db import models
from authapp.models import MainUser

# Create your models here.


class QuizQuestions(models.Model):
    question = models.CharField(max_length=1000)
    explanation = models.CharField(max_length=2000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class QuizOptions(models.Model):
    question = models.ForeignKey(QuizQuestions,related_name='options',on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

class QuizAttempt(models.Model):
    user = models.ForeignKey(MainUser,on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestions,on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOptions, null=True, blank=True, on_delete=models.SET_NULL)
    points = models.PositiveSmallIntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True,blank=True)
    