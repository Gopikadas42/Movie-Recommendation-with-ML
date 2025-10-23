from MovieRecommend import views
from django.urls import path

urlpatterns = [

    path('user_register/',views.user_register),
    path('login/',views.login_view),
    path('profile/',views.profile_view),
    path('search/',views.search_movies),
    path('movies/',views.movie_list),
    path('single/<int:id>',views.single_movie),
    path('add_movie/',views.add_movie),
    path('update/<int:id>',views.update_movie),
    path('delete/<int:id>',views.delete_movie),
    path('add_review/<int:id>',views.add_review),
    path('update_review/<int:id>',views.update_review),
    path('delete_review/<int:id>',views.delete_review),
    path('list_movie_review/<int:id>',views.list_movie_reviews),
    path('watchedmovies/',views.mark_movie_as_watched),
    path('movies/recommended/', views.recommended_movies, name='recommended_movies'),

]