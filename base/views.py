from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea
from django.views.generic import TemplateView
import calendar
from django.http import HttpResponse
from datetime import datetime

def mostrar_calendario(request):
    mes = int(request.GET.get('mes', datetime.now().month))
    año = int(request.GET.get('año', datetime.now().year))

    if mes < 1 or mes > 12:
        mes = datetime.now().month
    if año < 1900 or año > 2100:
        año = datetime.now().year

    tareas = Tarea.objects.filter(fecha__month=mes, fecha__year=año)
    cal = calendar.Calendar(firstweekday=6)
    semanas = cal.monthdayscalendar(año, mes)

    tareas_por_dia = {}
    for tarea in tareas:
        dia = tarea.fecha.day
        if dia not in tareas_por_dia:
            tareas_por_dia[dia] = {'tareas': [], 'completas': 0}
        tareas_por_dia[dia]['tareas'].append(tarea)
        if tarea.completo:
            tareas_por_dia[dia]['completas'] += 1

    # Función para comprobar si todas las tareas están completas
    for dia, info in tareas_por_dia.items():
        if info['completas'] == len(info['tareas']):
            tareas_por_dia[dia]['all_complete'] = True
        else:
            tareas_por_dia[dia]['all_complete'] = False

    # Obtener el nombre del mes
    mes_nombre = calendar.month_name[mes]

    # Calcular los meses anterior y siguiente
    mes_anterior = mes - 1 if mes > 1 else 12
    mes_siguiente = mes + 1 if mes < 12 else 1
    año_anterior = año - 1 if mes == 1 else año
    año_siguiente = año + 1 if mes == 12 else año

    return render(request, 'base/calendar.html', {
        'semanas': semanas,
        'mes': mes,
        'año': año,
        'mes_nombre': mes_nombre,
        'tareas_por_dia': tareas_por_dia,
        'mes_anterior': mes_anterior,
        'año_anterior': año_anterior,
        'mes_siguiente': mes_siguiente,
        'año_siguiente': año_siguiente,
    })

def detalles_dia(request, dia, mes, año):
    # Verifica que el día, mes y año sean válidos
    try:
        dia = int(dia)
        mes = int(mes)
        año = int(año)
        fecha = datetime(año, mes, dia)
    except ValueError:
        return render(request, 'base/404.html', status=404)

    # Obtiene las tareas para el día especificado
    tareas = Tarea.objects.filter(fecha=fecha)

    return render(request, 'base/dia.html', {
        'dia': dia,
        'mes': mes,
        'año': año,
        'tareas': tareas
    })

class Logueo(LoginView):
    template_name = "base/login.html"
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')  # Redirige a la página de inicio

class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super(PaginaRegistro, self).get(*args, **kwargs)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'base/home.html'
    context_object_name = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Aquí puedes agregar más datos relacionados con otras funcionalidades
        return context

class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea
    context_object_name = 'tareas'

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()

        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context

class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'
    template_name = 'base/tarea.html'

class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo', 'fecha']  # Asegúrate de incluir 'fecha'
    success_url = reverse_lazy('tareas')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)

class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'descripcion', 'completo', 'fecha']  # Asegúrate de incluir 'fecha'
    success_url = reverse_lazy('tareas')

class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')

