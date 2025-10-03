from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie, MovieList
from .services import *

def movies(request):
    popular_movies = get_popular_movies()
    return render(request, "movies/movies.html", {"movies": popular_movies})

def movie_search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = get_movies_by_title(query)
    return render(request, "movies/movie_search.html", {"results": results, "query": query})

def movie_details(request, movie_id):
    movie = get_movie_details(movie_id)
    return render(request, "movies/movie_details.html", {"movie": movie})

@login_required
def user_lists(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        if name:
            MovieList.objects.create(owner=request.user, name=name, description=description)
            return redirect("user_lists")
    
    lists = MovieList.objects.filter(owner=request.user)
    return render(request, "movies/user_lists.html", {"lists": lists})

@login_required
def user_profile(request):
    user = request.user
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        if name:
            MovieList.objects.create(owner=user, name=name, description=description)
            return redirect("user_profile")

    lists = MovieList.objects.filter(owner=user)
    context = {
        "user": user,
        "lists": lists,
    }
    return render(request, "movies/user_profile.html", context)
