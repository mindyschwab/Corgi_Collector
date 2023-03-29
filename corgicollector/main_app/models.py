from django.db import models
from django.urls import reverse

MEALS = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening')
)
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


class Feeding(models.Model):
    date = models.DateField('feeding Date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0])

    # if a cat gets deleted, delete all of it's feedings
    corgi = models.ForeignKey(Corgi, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_meal_display()} on {self.date}'
