import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Avg, Count
from .models import Movie, Review


def get_recommendations(user_id, top_n=10):
    """
    Content-based recommendation system:
    - Uses TF-IDF on movie genres and descriptions
    - Weights by user's ratings
    - Excludes movies already reviewed by the user
    """
    user_reviews = Review.objects.filter(user_id=user_id)

    # Fallback if user has no reviews
    if not user_reviews.exists():
        return get_popular_movies(top_n)

    # Prepare movie data
    all_movies = Movie.objects.prefetch_related('genres').all()
    if not all_movies.exists():
        return []

    movie_ids = []
    movie_texts = []

    for movie in all_movies:
        movie_ids.append(movie.id)
        # Combine genres + description for better content similarity
        genre_text = " ".join([g.genre for g in movie.genres.all()])
        movie_texts.append(genre_text + " " + movie.description)

    # TF-IDF vectorization
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movie_texts)

    # Cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Get movies liked by user (rating >= 4)
    liked_reviews = [r for r in user_reviews if r.rating >= 4]
    if not liked_reviews:
        return get_popular_movies(top_n)

    movie_scores = {}
    similarity_threshold = 0.1

    for review in liked_reviews:
        liked_movie_id = review.movie_id
        liked_rating = review.rating

        if liked_movie_id in movie_ids:
            idx = movie_ids.index(liked_movie_id)
            sim_scores = list(enumerate(cosine_sim[idx]))

            for i, score in sim_scores:
                if score <= similarity_threshold:
                    continue

                movie_id = movie_ids[i]

                # Skip already reviewed movies
                if movie_id == liked_movie_id or movie_id in [r.movie_id for r in user_reviews]:
                    continue

                # Weighted score by rating
                movie_scores[movie_id] = movie_scores.get(movie_id, 0) + (score * liked_rating)

    # Sort movies by score
    recommended = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]

    if recommended:
        return [mid for mid, _ in recommended]
    else:
        return get_popular_movies(top_n)


def get_popular_movies(top_n=10):
    """
    Fallback: Top-rated & most-reviewed movies
    """
    popular = (
        Movie.objects.annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        .filter(review_count__gte=1)
        .order_by('-avg_rating', '-review_count')[:top_n]
    )

    return [m.id for m in popular]
