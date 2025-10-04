from django.urls import path
from . import views

urlpatterns = [
    path("", views.movies, name="movies"),
    path("movie/<int:movie_id>/", views.movie_details, name="movie_details"),

    path('user/lists/', views.user_lists, name='user_lists'),
    path('user/lists/<int:list_id>/', views.view_list, name='view_list'),
    path('user/lists/<int:list_id>/edit/', views.edit_list, name='edit_list'),
    path('user/lists/<int:list_id>/delete/', views.delete_list, name='delete_list'),
    path('user/lists/<int:list_id>/remove-movie/<int:movie_id>/', views.remove_movie_from_list, name='remove_movie_from_list'),

    path("movie/<int:movie_id>/", views.movie_details, name="movie_details"),
    path('movie/<int:movie_id>/select_list/', views.select_list, name='select_list'),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
]
