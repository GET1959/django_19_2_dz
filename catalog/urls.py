from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import CatalogConfig
from catalog.views import (
    HomeView,
    ProductListView,
    ProductDetailView,
    ContactView,
    CategoryListView,
    CategoryView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    VersionListView,
    VersionDeleteView,
)

app_name = CatalogConfig.name


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("product/", ProductListView.as_view(), name="product"),
    path("product/<int:pk>/", cache_page(60)(ProductDetailView.as_view()), name="product_<int:pk>"),
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("categories/<int:pk>/", CategoryView.as_view(), name="categories"),
    path("product/create", ProductCreateView.as_view(), name="product_create"),
    path("product/update/<int:pk>", never_cache(ProductUpdateView.as_view()), name="product_update"),
    path("product/delete/<int:pk>", ProductDeleteView.as_view(), name="product_delete"),
    path("versions/", VersionListView.as_view(), name="versions"),
    path(
        "versions/delete/<int:pk>", VersionDeleteView.as_view(), name="version_delete"
    ),
]
