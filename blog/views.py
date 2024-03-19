from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Article


class ArticleCreateView(CreateView):
    model = Article
    fields = ('title', 'slug', 'body', 'preview', 'is_published', 'views_count')
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            article = form.save()
            article.slug = slugify(article.title)
            article.save()

        return super().form_valid(form)


class ArticleListView(ListView):
    model = Article
    extra_context = {
        'title': 'Публикация'
    }

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class ArticleUpdateView(UpdateView):
    model = Article
    fields = ('title', 'slug', 'body', 'preview', 'is_published', 'views_count')
    # success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            article = form.save()
            article.slug = slugify(article.title)
            article.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class ArticleDeleteView(DeleteView):
    model = Article
    success_url = reverse_lazy('blog:list')
