from django.urls import path
from . import api_views


urlpatterns = [
    path('tasks/', api_views.TaskListCreateAPIView.as_view(), name='api-task-list'),
    path('tasks/<int:pk>/', api_views.TaskDetailAPIView.as_view(), name='api-task-detail'),
]
