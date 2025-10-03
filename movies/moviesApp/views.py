from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from .services import *

def movies(request):
    popular_movies = get_popular_movies()
    return render(request, "movies/movies.html", {"movies": popular_movies})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies/movie_list.html", {"movies": movies})

def movie_search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = search_movies(query)

    movies = Movie.objects.all()
    return render(request, "movies/movies.html", {"movies": movies, "results": results, "query": query})