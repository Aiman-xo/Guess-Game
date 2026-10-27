from django.urls import path
from .views import RegisterView,LoginView,CookieRefreshView,HealthCheck

urlpatterns=[
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('refresh/',CookieRefreshView.as_view(),name='new_access_token'),
    path('health/',HealthCheck.as_view(),name='new_access_token'),
]