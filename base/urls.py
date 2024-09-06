from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import ListaPendientes, DetalleTarea, CrearTarea, EditarTarea, EliminarTarea, Logueo, PaginaRegistro, HomeView

urlpatterns = [
    # Página de inicio multifuncional
    path('', HomeView.as_view(), name='home'),

    # Aplicación de Tareas
    path('tareas/', ListaPendientes.as_view(), name='tareas'),
    path('tarea/<int:pk>', DetalleTarea.as_view(), name='tarea'),
    path('crear-tarea/', CrearTarea.as_view(), name='crear-tarea'),
    path('editar-tarea/<int:pk>', EditarTarea.as_view(), name='editar-tarea'),
    path('eliminar-tarea/<int:pk>', EliminarTarea.as_view(), name='eliminar-tarea'),

    # Autenticación
    path('login/', Logueo.as_view(), name='login'),
    path('registro/', PaginaRegistro.as_view(), name='registro'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # Otras funcionalidades (calendario, asistente virtual, calculadora)
    # Se agregarán en el futuro
]
