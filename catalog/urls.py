from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import (
    ProductCreateView,
    ProductListView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    VersionUpdateView,
)

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="products_list"),
    path(
        "products/<int:pk>/",
        ProductDetailView.as_view(),
        name="products_detail",
    ),
    path(
        "versions/<int:pk>/update/",
        VersionUpdateView.as_view(),
        name="version_update",
    ),
    path(
        "products/create/", ProductCreateView.as_view(), name="products_create"
    ),
    path(
        "products/<int:pk>/update/",
        ProductUpdateView.as_view(),
        name="products_update",
    ),
    path(
        "products/<int:pk>/delete/",
        ProductDeleteView.as_view(),
        name="products_delete",
    ),
]
