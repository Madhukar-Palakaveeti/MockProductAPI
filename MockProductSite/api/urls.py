from django.urls import path
from api import views

urlpatterns = [
    path('get-product/', views.product_list, name='get-product'),
    path('create-product/', views.create_product, name='create-product'),
    path('update-product/<int:pk>/', views.update_product, name='update-product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),
    path('', views.get_product_urls)
]