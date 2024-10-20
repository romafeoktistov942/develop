from django.db.models.base import Model as Model
from django.forms import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ProductForm, ProductModeratorForm, VersionForm
from .models import Product, Version
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductListView(LoginRequiredMixin, ListView):
    model = Product


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manufacturer"] = self.object.manufacturer
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

    def get_success_url(self) -> str:
        return reverse("catalog:products_detail", args=[self.kwargs.get("pk")])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            formset = VersionFormset(self.request.POST, instance=self.object)
            context_data["formset"] = formset
        else:
            formset = VersionFormset(instance=self.object)
            context_data["formset"] = formset

        context_data["formset"].queryset = self.object.versions.all()

        return context_data

    def product_list(request):
        products = Product.objects.all()
        for product in products:
            product.active_versions = product.versions.filter(is_active=True)
        context = {
            "products": products,
        }
        return render(request, "product_list.html", context)

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data["formset"]
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )

    def get_form_class(self):
        user = self.request.user
        if user == self.object.manufacturer:
            return ProductForm
        if (
            user.has_perm("catalog.can_edit_is_published")
            and user.has_perm("catalog.can_edit_description")
            and user.has_perm("catalog.can_edit_category")
        ):
            return ProductModeratorForm
        raise PermissionDenied


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products_list")


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = "catalog/version_form.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
