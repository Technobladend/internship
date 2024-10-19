from django.urls import path
from . import views

urlpatterns = [
    path('task/', views.task_list_api_view),
    path('task/<int:id>/', views.task_detail_api_view),
]