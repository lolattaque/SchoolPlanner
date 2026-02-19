from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('task/edit/<int:task_id>/', views.edit_task, name='edit_task'),

]
