from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)

from catalog.forms import ContactForm, ProductForm, VersionForm
from catalog.models import Product, Category, Version


class HomeView(TemplateView):
    template_name = "catalog/product_list.html"
    extra_context = {"title": "Главная страница"}

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["object_list"] = Product.objects.all()[:3]
        return context_data


class ContactView(LoginRequiredMixin, FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = "/product/"

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def form_valid(self, form):
        return super().form_valid(form)


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    extra_context = {"title": "Products"}
    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["version"] = Version.objects.filter(
            product_id=self.kwargs.get("pk"), version_sign=True
        ).last()
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    extra_context = {"title": "Categories"}

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"


class CategoryView(LoginRequiredMixin, ListView):
    model = Product

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(category_id=self.kwargs.get("pk"))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get("pk"))
        context_data["category.pk"] = category_item.pk
        context_data["title"] = f"Товары категории {category_item.category}"
        return context_data


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product")

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:product")

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            # instances = formset.save(commit=False)
            # self.object.current_version = str(instances[-1])[-1]
            # formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:product")

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"


class VersionListView(LoginRequiredMixin, ListView):
    model = Version
    extra_context = {"title": "Versions"}

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"


class VersionDeleteView(DeleteView):
    model = Version
    success_url = reverse_lazy("catalog:versions")
