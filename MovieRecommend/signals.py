from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WatchedMovies, Movie

@receiver(post_save, sender=WatchedMovies)
def increase_movie_views_count(sender, instance, created, **kwargs):
    if created:  # Only when a new watched record is created
        movie = instance.movie
        movie.watched_count += 1
        movie.save()