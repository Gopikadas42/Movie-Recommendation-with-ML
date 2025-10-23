
from django.db import models
from rest_framework.fields import ImageField
from django.contrib.auth.models import AbstractUser


# Create your models here.

class MyUser(AbstractUser):
    bio=models.TextField(blank=True,null=True)
    profile_pic=models.ImageField(upload_to='profile/',null=True)
    age=models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Genre(models.Model):
    genre=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.genre

class Movie(models.Model):
    movie_title=models.CharField(max_length=300)
    description=models.TextField()
    genres = models.ManyToManyField(Genre)
    director=models.CharField(max_length=200)
    released_at=models.DateField()
    watched_count=models.IntegerField(default=0)
    duration=models.IntegerField()
    poster_url = models.URLField(blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0,max_length=5)


    def __str__(self):
        return self.movie_title

class Review(models.Model):
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating =models.FloatField(default=0, max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.movie_title}'



class WatchedMovies(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name="users")
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movies" ,null=True)



