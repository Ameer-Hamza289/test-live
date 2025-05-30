from django.db import models
from django.utils import timezone

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    car_id = models.IntegerField(default=0)
    customer_need = models.CharField(max_length=100, blank=True)
    car_title = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    user_id = models.IntegerField(default=0, blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email
