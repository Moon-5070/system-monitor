from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/status/', views.status_api, name='status_api'),
]
