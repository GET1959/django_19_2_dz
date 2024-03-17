from django.views.generic import TemplateView, ListView, DetailView, FormView

from catalog.forms import ContactForm
from catalog.models import Product, Category


class HomeView(TemplateView):
    template_name = 'catalog/product_list.html'
    extra_context = {
        'title': 'Главная страница'
    }

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['object_list'] = Product.objects.all()[:3]
        return context_data


class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/product/'

    def form_valid(self, form):
        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Products'
    }


class ProductDetailView(DetailView):
    model = Product

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.save()
        return self.object


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Categories'
    }


class CategoryView(ListView):
    model = Product

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category.pk'] = category_item.pk
        context_data['title'] = f'Товары категории {category_item.category}'
        return context_data
