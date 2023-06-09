from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

MEALS = (
    ('M', 'Morning'),
    ('E', 'Evening')
)
# Create your models here.


class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    description = models.TextField(max_length=200, default='')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk': self.id})


class Corgi(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    # Adding many to many relationship with toys
    toys = models.ManyToManyField(Toy)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# changing this instance method doesn't impact the database
# therefore, we don't need to run makemigrations or migrate
    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'corgi_id': self.id})

    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)


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

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    corgi = models.ForeignKey(Corgi, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for corgi_id: {self.corgi_id} @{self.url}"
