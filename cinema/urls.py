from django.urls import path, include
from cinema import views

urlpatterns = [
    path('list/', views.movies_list_page, name='movies_list'),
    path('add/', views.add_cinema_page, name='add_movie'),
    path('<int:pk>/details', views.MovieDetailView.as_view(), name='movie_detail'),
    path('<int:pk>/update', views.MovieUpdateView.as_view(), name='movie_update'),
    path('<int:pk>/delete', views.MovieDeleteView.as_view(), name='movie_delete'),
    path("sessions/<movie_id>/create", views.SessionCreateView.as_view(), name="session_create"),
    path('review/<int:pk>/delete', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('review/<int:pk>/update', views.ReviewUpdateView.as_view(), name='review_update'),
]
