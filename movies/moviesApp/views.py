from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from .services import search_movies

def movies(request):
    return render(request, "movies/movies.html")

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, "movies/movie_list.html", {"movies": movies})

def movie_search(request):
    query = request.GET.get("q")
    results = []
    if query:
        results = search_movies(query)
    return render(request, "movies/movie_search.html", {"results": results, "query": query})

def movie_detail(request, movie_id){
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, "movie_detail.html", {"movie": movie})
}