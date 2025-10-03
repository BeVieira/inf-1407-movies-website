import requests
from django.conf import settings

API_BASE_URL = "https://api.themoviedb.org/3"
API_KEY = settings.TMDB_API_KEY

def search_movies(query):
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