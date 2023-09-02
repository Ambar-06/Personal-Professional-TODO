from . import views
from django.urls import path

urlpatterns = [
    path('signup/', views.signup_f, name='signup'),
    path('login/', views.login_f, name='login'),
    path('home/', views.home_f, name='home'),
    path('logout/', views.logout_f, name='logout'),
]
