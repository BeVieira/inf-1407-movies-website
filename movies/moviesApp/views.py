from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from .models import Movie, MovieList
from .services import *

def movies(request):
    query = request.GET.get("q")
    if query:
      results = get_movies_by_title(query)
      return render(request, "movies/movies.html", {"results": results, "query": query})
    popular_movies = get_popular_movies()
    context = {"movies": popular_movies}
    if request.user.is_authenticated:
        user_lists = MovieList.objects.filter(owner=request.user)
        context["user_lists"] = user_lists
    return render(request, "movies/movies.html", context)

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
def view_list(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id, owner=request.user)
    movies = movie_list.movies.all() 
    return render(request, "movies/view_list.html", {"movie_list": movie_list, "movies": movies})

@login_required
def edit_list(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id, owner=request.user)
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description", "")
        if name:
            movie_list.name = name
            movie_list.description = description
            movie_list.save()
            return redirect("user_lists")
    
    return render(request, "movies/edit_list.html", {"movie_list": movie_list})


@login_required
def delete_list(request, list_id):
    movie_list = get_object_or_404(MovieList, id=list_id, owner=request.user)
    
    if request.method == "POST":
        movie_list.delete()
        return redirect("user_lists")
    
    return render(request, "movies/delete_list_confirm.html", {"movie_list": movie_list})


@login_required
def remove_movie_from_list(request, list_id, movie_id):
    movie_list = get_object_or_404(MovieList, id=list_id, owner=request.user)
    movie = get_object_or_404(Movie, id=movie_id)
    
    if movie in movie_list.movies.all():
        movie_list.movies.remove(movie)
    
    return redirect('view_list', list_id=list_id)

@login_required
def select_list(request, movie_id):
    if request.method == "POST":
        list_id = request.POST.get("list_id")
        movie_list = get_object_or_404(MovieList, id=list_id, owner=request.user)
        
        api_data = get_movie_details(movie_id)  
        movie = save_movie_from_api(api_data)
        
        movie_list.movies.add(movie)

        messages.success(request, f'O filme "{movie.title}" foi adicionado à lista "{movie_list.name}"!')
        
        return redirect("movie_details", movie_id=movie_id)

    return redirect("movie_details", movie_id=movie_id)

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