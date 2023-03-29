from django.db import models
from django.urls import reverse

# Create your models here.


class Corgi(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

# changing this instance method doesn't impact the database
# therefore, we don't need to run makemigrations or migrate
    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'corgi_id': self.id})
