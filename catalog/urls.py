from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts

app_name = CatalogConfig

urlpatterns = [
    path("", home, name="home"),
    path("", contacts, name="contacts"),
]
