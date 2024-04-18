from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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

from catalog.forms import ContactForm, ProductForm, VersionForm, ProductModeratorForm
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

    # def get_queryset(self):
    #     return super().get_queryset().filter(owner=self.request.user)


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


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.add_product'
    success_url = reverse_lazy("catalog:product")

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    permission_required = 'catalog.change_product'
    success_url = reverse_lazy("catalog:product")

    login_url = "/users/auth_request"
    redirect_field_name = "users/auth_request"

    def has_permission(self):
        product = self.get_object()
        is_moderator = self.request.user.groups.filter(name='moderator').exists()
        is_owner = product.has_change_permission(self.request.user)
        return is_moderator or is_owner

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data["formset"] = VersionFormset(instance=self.object)
        return context_data

    def get_form_class(self):
        product = self.get_object()
        is_moderator = self.request.user.groups.filter(name='moderator').exists()
        is_owner = product.has_change_permission(self.request.user)
        if is_moderator and not is_owner:
            return ProductModeratorForm
        return ProductForm

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    permission_required = 'catalog.delete_product'
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
