from .models import Genre,MyUser,Movie,Review,WatchedMovies
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields='__all__'

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model=Genre
        fields='__all__'

class MovieSerializer(serializers.ModelSerializer):
    genres=GenreSerializer(read_only=True,many=True)
    genres_id=serializers.PrimaryKeyRelatedField(queryset=Genre.objects.all(),source="genres",many=True,write_only=True)

    class Meta:
        model=Movie
        fields='__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    movie=MovieSerializer(read_only=True)
    movie_id=serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(),source="movie",write_only=True)

    class Meta:
        model=Review
        fields='__all__'


class ReviewDisplaySerializer(serializers.ModelSerializer):
    username = UserSerializer(read_only=True)
    movie_title = MovieSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['movie_title', 'username', 'title', 'comment', 'rating']


class WatchedMoviesSerializer(serializers.ModelSerializer):
    movie=MovieSerializer(read_only=True)
    movie_id=serializers.PrimaryKeyRelatedField(queryset=Movie.objects.all(),source="movie",write_only=True)

    class Meta:
        model=WatchedMovies
        fields='__all__'