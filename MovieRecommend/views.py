from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from .serializers import UserSerializer,GenreSerializer,MovieSerializer,ReviewSerializer,ReviewDisplaySerializer
from .models import Movie,Genre,MyUser,Review,WatchedMovies
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from .recommendation_engine import get_recommendations

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def user_register(request):
    name=request.data.get('username')
    password=request.data.get('password')
    first_name=request.data.get('first_name')
    last_name=request.data.get('last_name')
    email=request.data.get('email')
    bio=request.data.get('bio')
    age=request.data.get('age')
    profile_pic=request.FILES.get('profile_pic')
    if not name or not password:
        return Response('Username and password are required')

    if MyUser.objects.filter(username=name).exists():
        return Response('Username already exists')

    user = MyUser.objects.create_user(username=name, password=password,first_name=first_name,last_name=last_name,email=email,bio=bio,age=age,profile_pic=profile_pic)
    return Response('User created successfully')

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    name=request.data.get('username')
    password=request.data.get("password")
    user=authenticate(username=name,password=password)
    if user is None:
        return Response({'errors':'invalid credentials'})
    refresh=RefreshToken.for_user(user)
    return Response({"refresh":str(refresh),"access":str(refresh.access_token)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user_obj=request.user
    serializer=UserSerializer(user_obj,many=False)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_movies(request):
    query = request.query_params.get('q', '')
    movies = Movie.objects.filter(
        Q(movie_title__icontains=query) |
        Q(description__icontains=query) |
        Q(director__icontains=query)
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    movie=Movie.objects.all()
    movie_serializer=MovieSerializer(movie,many=True)
    return Response(movie_serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_movie(request,id):
    try:
        movie=Movie.objects.get(id=id)
        movie_serializer=MovieSerializer(movie,many=False)
        return Response(movie_serializer.data)
    except Movie.DoesNotExist:
        return Response('no such movie')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_movie(request):
    movie_serializer=MovieSerializer(data=request.data)
    if movie_serializer.is_valid():
        movie_serializer.save()
        return Response('Movie Created Succesfully')
    else:
        return Response(movie_serializer.errors)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_movie(request,id):
    try:
        movie=Movie.objects.get(id=id)
        movie.delete()
        return Response('movie is deleted...')
    except Movie.DoesNotExist:
        return Response('movie not allow..........')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_movie(request,id):
    try:
        update_object = Movie.objects.get(id=id)
        movie_serializer = MovieSerializer(data=request.data, instance=update_object, partial=True)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Response('Movie updated successfully')
        else:
            return Response(movie_serializer.errors)
    except Movie.DoesNotExist:
        return Response('Movie not found')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request,id):
    try:
        movie = Movie.objects.get(id=id)
        if Review.objects.filter(user=request.user,movie=movie).exists():
            return Response("already reviewed this movie")
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, movie=movie)
            return Response('Review added successfully')
        else:
            return Response(serializer.errors)
    except Movie.DoesNotExist:
        return Response('Movie not found')




@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_review(request,id):
    try:
        review = Review.objects.get(id=id, user=request.user)
    except Review.DoesNotExist:
        return Response('Review not found or permission denied')

    serializer = ReviewSerializer(instance=review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response('Review updated successfully')
    else:
        return Response(serializer.errors)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,id):
    try:
        review = Review.objects.get(id=id, user=request.user)
    except Review.DoesNotExist:
        return Response( "Review not found or not yours")
    review.delete()
    return Response( "Review deleted successfully")

@api_view(['GET'])
@permission_classes([AllowAny])
def list_movie_reviews(request,id):
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response('Movie not found')

        reviews = Review.objects.filter(movie=movie)
        serializer = ReviewDisplaySerializer(reviews, many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_movie_as_watched(request):
    try:
        movie_id = request.data.get('movie_id')
        if not movie_id:
            return Response({"error": "movie_id is required"}, status=400)

        movie = Movie.objects.get(id=movie_id)

        # Check if already watched by the user
        if WatchedMovies.objects.filter(user=request.user, movie=movie).exists():
            return Response({"message": "Already marked as watched"})

        # Creating this will trigger the signal
        WatchedMovies.objects.create(user=request.user, movie=movie)

        return Response({"message": "Movie marked as watched"})

    except Movie.DoesNotExist:
        return Response({"error": "Movie not found"}, status=404)
    except Exception as error:
        return Response({"error": str(error)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_movies(request):
    """
    Return personalized movie recommendations for logged-in user
    """
    rec_ids = get_recommendations(request.user.id)
    movies = Movie.objects.filter(id__in=rec_ids)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

