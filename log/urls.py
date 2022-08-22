
from django.urls import path

from . import views

app_name = 'logs'

urlpatterns = [
    path('logs/', views.LogsViewLogs.as_view(),name='logs'),
    path('logs/search', views.LogsSearchLogs.as_view(),name='search_logs'),
]
