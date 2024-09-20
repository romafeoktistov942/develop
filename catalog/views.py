from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product


class ProductListView(ListView):
    model = Product


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    model = Product
    fields = ("name", "description", "image", "category", "price")
    success_url = reverse_lazy("catalog:products_list")


class ProductUpdateView(UpdateView):
    model = Product
    fields = ("name", "description", "image", "category", "price")
    success_url = reverse_lazy("catalog:products_list")

    def get_success_url(self) -> str:
        return reverse("catalog:products_detail", args=[self.kwargs.get("pk")])



class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products_list")