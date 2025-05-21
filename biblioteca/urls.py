from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'biblioteca'

urlpatterns = [
    path('', views.LibroListView.as_view(), name='libro-list'),
    path('libro/<int:pk>/', views.LibroDetailView.as_view(), name='libro-detail'),
    path('libro/nuevo/', views.LibroCreateView.as_view(), name='libro-create'),
    path('libro/<int:pk>/editar/', views.LibroUpdateView.as_view(), name='libro-update'),
    path('libro/<int:pk>/prestar/', views.PrestarLibroView.as_view(), name='libro-prestar'),
    path('libro/<int:pk>/devolver/', views.DevolverLibroView.as_view(), name='libro-devolver'),
    path('mis-libros/', views.MisLibrosPrestadosView.as_view(), name='mis-libros'),
]

