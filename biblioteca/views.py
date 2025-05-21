from django.views.generic import View,ListView, DetailView,CreateView, UpdateView
from .models import Libro
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from rest_framework import viewsets, permissions,status
from .serializers import LibroSerializer, UsuarioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


class LibroListView(ListView):
    model = Libro
    template_name = 'biblioteca/libro_list.html'
    context_object_name = 'libros'

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'biblioteca/libro_detail.html'
    context_object_name = 'libro'

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'admin'

class LibroCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Libro
    fields = ['titulo', 'autor', 'anio_publicacion', 'cantidad_stock']
    template_name = 'biblioteca/libro_form.html'
    success_url = reverse_lazy('biblioteca:libro-list')

class LibroUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = Libro
    fields = ['titulo', 'autor', 'anio_publicacion', 'cantidad_stock']
    template_name = 'biblioteca/libro_form.html'
    success_url = reverse_lazy('biblioteca:libro-list')
    
class RegularRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.rol == 'regular'

class PrestarLibroView(LoginRequiredMixin, RegularRequiredMixin, View):
    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        # Verificamos si el usuario ya tiene prestado ese libro
        if libro in request.user.libros_prestados.all():
            messages.warning(request, "Ya tienes este libro prestado.")
        elif libro.cantidad_stock > 0:
            request.user.libros_prestados.add(libro)
            libro.cantidad_stock -= 1
            libro.save()
            messages.success(request, "Libro prestado con éxito.")
        else:
            messages.warning(request, "No hay stock disponible.")

        return redirect('biblioteca:libro-detail', pk=pk)
    
class DevolverLibroView(LoginRequiredMixin, RegularRequiredMixin, View):
    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        if libro in request.user.libros_prestados.all():
            request.user.libros_prestados.remove(libro)
            libro.cantidad_stock += 1
            libro.save()
            messages.success(request, "Libro devuelto con éxito.")
        else:
            messages.warning(request, "Este libro no estaba prestado.")
        return redirect('biblioteca:libro-detail', pk=pk)
    
class MisLibrosPrestadosView(LoginRequiredMixin, RegularRequiredMixin, ListView):
    template_name = 'biblioteca/mis_libros.html'
    context_object_name = 'libros'

    def get_queryset(self):
        return self.request.user.libros_prestados.all()

class EsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'

class EsUsuarioRegular(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'regular'

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [EsAdmin()]
        elif self.action in ['prestar', 'devolver']:
            return [EsUsuarioRegular()]
        return [permissions.IsAuthenticated()]
    @action(detail=True, methods=['post'], url_path='prestar')
    def prestar(self, request, pk=None):
        libro = self.get_object()
        user = request.user

        if libro in user.libros_prestados.all():
            return Response({'detail': 'Ya tienes este libro prestado.'}, status=status.HTTP_400_BAD_REQUEST)

        if libro.cantidad_stock > 0:
            user.libros_prestados.add(libro)
            libro.cantidad_stock -= 1
            libro.save()
            return Response({'detail': 'Libro prestado con éxito.'})
        return Response({'detail': 'No hay stock disponible.'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='devolver')
    def devolver(self, request, pk=None):
        libro = self.get_object()
        user = request.user

        if libro in user.libros_prestados.all():
            user.libros_prestados.remove(libro)
            libro.cantidad_stock += 1
            libro.save()
            return Response({'detail': 'Libro devuelto con éxito.'})
        return Response({'detail': 'Este libro no estaba prestado.'}, status=status.HTTP_400_BAD_REQUEST)
