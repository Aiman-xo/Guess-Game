from django.urls import path
from .views import QuizView,LeaderBoardView

urlpatterns=[
    path('quiz/question/',QuizView.as_view(),name='question'),
    path('quiz/leaderboard/',LeaderBoardView.as_view(),name='leaderboard'),
]