import requests
from .models import Movie
from django.conf import settings

API_BASE_URL = "https://api.themoviedb.org/3"
API_KEY = settings.TMDB_API_KEY

def get_movies_by_title(query):
    url = f"{API_BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": query,
        "language": "pt-BR"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_popular_movies():
    url = f"{API_BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_movie_details(movie_id):
    url = f"{API_BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "pt-BR"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

    from .models import Movie

def save_movie_from_api(api_data):
    title = api_data.get("title", "")
    year = int(api_data.get("release_date", "0000")[:4]) if api_data.get("release_date") else None
    runtime = str(api_data.get("runtime", ""))
    genres = ", ".join([g["name"] for g in api_data.get("genres", [])])
    language = api_data.get("original_language", "")
    rating = str(api_data.get("vote_average", ""))
    plot = api_data.get("overview", "")
    poster = api_data.get('poster_path', '')

    movie, created = Movie.objects.get_or_create(
        title=title,
        year=year,
        defaults={
            "runtime": runtime,
            "genre": genres,
            "language": language,
            "rating": rating,
            "plot": plot,
            "poster": poster
        }
    )

    return movie