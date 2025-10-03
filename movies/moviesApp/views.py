from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
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


def login_view(request):
    if request.user.is_authenticated:
        return redirect('movies')  # redireciona para a página principal

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login realizado com sucesso.")
            return redirect('movies')
        else:
            messages.error(request, "Credenciais inválidas. Verifique e tente novamente.")
    else:
        form = AuthenticationForm(request)

    return render(request, "auth/login.html", {"form": form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('movies')

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Conta criada e logado com sucesso.")
            return redirect('movies')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = SignUpForm()

    return render(request, "auth/signup.html", {"form": form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Você saiu da sua conta.")
        return redirect('movies')
    # permitir logout via GET se preferir:
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('movies')