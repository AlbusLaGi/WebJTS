from django.urls import path
from . import views  # Importa las vistas de la app actual
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Cuando alguien visite la URL "raíz" de esta app, se ejecutará la vista 'home'
    path('', views.home, name='home'),
    path('quienes-somos/', views.about, name='about'),
    path('eventos/', views.eventos_list, name='eventos'),
    path('eventos/<slug:evento_slug>/', views.evento_detalle, name='evento_detalle'),
    path('eventos/<slug:evento_slug>/inscripcion/', views.inscribir_evento, name='inscribir_evento'),


    path('api/get_inscripcion_data_by_cedula/', views.get_inscripcion_data_by_cedula, name='get_inscripcion_data_by_cedula'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]