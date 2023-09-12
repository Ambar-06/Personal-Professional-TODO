from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup_f, name='signup'),
    path('login/', views.login_f, name='login'),
    path('home/', views.home_f, name='home'),
    path('logout/', views.logout_f, name='logout'),
    path('mark_as_complete/', views.mark_as_complete, name='mark_as_complete'),
    path('delete_task/', views.delete_task, name='delete_task'),
    path('edit_task/', views.delete_task, name='edit_task'),
]
