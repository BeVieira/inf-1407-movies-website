from django.urls import path
from . import views

urlpatterns = [
    path('', views.movies, name='movies'),
    path("search/", views.movie_search, name="movie_search"),
]
