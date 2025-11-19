from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.categorized_product_list, name='categorized_product_list'),
    path('all/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('packages/<slug:slug>/', views.package_detail, name='package_detail'),
    path('admin/import_products/', views.import_products_from_sheet, name='import_products_from_sheet'),
]