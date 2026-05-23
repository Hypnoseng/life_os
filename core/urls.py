from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),

    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/toggle/', views.toggle_task, name='toggle_task'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('api/tasks', views.TaskListCreateAPI.as_view(), name='task_list_api_no_slash'),
    path('api/tasks/', views.TaskListCreateAPI.as_view(), name='task_list_api'),
    path('api/tasks/<int:task_id>', views.task_detail_api, name='task_detail_api_no_slash'),
    path('api/tasks/<int:task_id>/', views.task_detail_api, name='task_detail_api'),
]
