from django.urls import path
from . import views

urlpatterns = [
    path('inquiry', views.inquiry, name='inquiry'),
    path('inquiry-no-csrf', views.inquiry_no_csrf, name='inquiry_no_csrf'),
    path('test-contact', views.test_contact, name='test_contact'),
    path('debug-contacts', views.contact_list_debug, name='contact_list_debug'),
]
