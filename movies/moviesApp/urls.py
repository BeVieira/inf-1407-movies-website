from django.urls import path
from . import views

urlpatterns = [
    path("", views.movies, name="movies"),
    path("search/", views.movie_search, name="movie_search"),
    path("movie/<int:movie_id>/", views.movie_details, name="movie_details"),

    path('user/lists/', views.user_lists, name='user_lists'),
    path('user/profile/', views.user_profile, name='user_profile'),
    path("movie/<int:movie_id>/", views.movie_details, name="movie_details"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]
