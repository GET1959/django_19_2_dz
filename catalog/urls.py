from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import HomeView, ProductListView, ProductDetailView, ContactView, CategoryListView, CategoryView

app_name = CatalogConfig.name


urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("product/", ProductListView.as_view(), name="product"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_<int:pk>"),
    path("categories/", CategoryListView.as_view(), name='category_list'),
    path("categories/<int:pk>/", CategoryView.as_view(), name='categories'),
]
