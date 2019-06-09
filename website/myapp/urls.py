from django.urls import path

from . import views

urlpatterns = [
    path('cinemas/', views.cinemas_render),
    path('movies/', views.movies_render),
    path('search/', views.search),
    path('check/', views.check),
    path('sign_up/', views.sign_up_view),
    path('logout/', views.logout_view),
    path('sign_in/', views.login),
    path('movie/<int:movie_id>/', views.movie_render),
    path('reserve/<int:movie_id>/', views.reserve),
    path('', views.index, name='index'),
]