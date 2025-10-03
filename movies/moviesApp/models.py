from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.IntegerField()
    runtime = models.CharField(max_length=50)
    genre = models.CharField(max_length=100)
    language = models.CharField(max_length=50, blank=True)
    rating = models.CharField(max_length=10, blank=True)
    plot = models.TextField(blank=True)
    poster = models.URLField(blank=True)
    
    def __str__(self):
        return self.title

class MovieList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    movies = models.ManyToManyField(Movie, blank=True)

    def __str__(self):
        return f"{self.name} - {self.owner.username}"
