from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<slug:slug>/', views.blog_detalle, name='detalle_post'),
    path('tipo/<str:tipo_contenido>/', views.blog_por_tipo, name='blog_por_tipo'),
]