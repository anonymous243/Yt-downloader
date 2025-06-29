from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/get-info/', views.get_info, name='get_info'),
    path('api/download/', views.download_video, name='download_video'),
]
