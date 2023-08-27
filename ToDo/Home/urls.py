from . import views
from django.urls import path

urlpatterns = [
    path('', views.test_f),
    path('signup/', views.signup_f, name='signup'),
    path('login/', views.login_f, name='login'),
]
