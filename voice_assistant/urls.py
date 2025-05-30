from django.urls import path
from . import views

app_name = 'voice_assistant'

urlpatterns = [
    path('', views.voice_assistant, name='talk-to-ai'),
    path('test/', views.test_api, name='test_api'),
    path('process/', views.process_voice, name='process_voice'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('refresh-inventory/', views.refresh_inventory, name='refresh_inventory'),
    path('test-cars/', views.test_cars_database, name='test_cars_database'),
] 