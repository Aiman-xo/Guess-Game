from django.contrib import admin
from .models import QuizQuestions,QuizOptions,QuizAttempt

# Register your models here.
admin.site.register(QuizOptions)
admin.site.register(QuizQuestions)
admin.site.register(QuizAttempt)