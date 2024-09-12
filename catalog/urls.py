from django.urls import path
from catalog.views import products_list, product_detail

app_name = 'catalog'

urlpatterns = [
    path("", products_list, name="products_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),
]