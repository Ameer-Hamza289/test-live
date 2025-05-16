from django.urls import path
from . import views

app_name = 'voice_assistant'

urlpatterns = [
    path('', views.voice_assistant, name='voice_assistant'),
    path('process/', views.process_voice, name='process_voice'),
    path('test-api/', views.test_api, name='test_api'),
] 