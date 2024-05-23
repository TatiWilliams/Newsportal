from django.views.generic import TemplateView, ListView
from django.views import generic
from .models import Post


class HomePageView(TemplateView):
    template_name = "flatpages/home.html"


class AboutPageView(TemplateView):
    template_name = "flatpages/about.html"


class NewsPageView(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = "flatpages/news.html"
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_list = context['news']
        for news in news_list:
            news.text = news.text[:20]
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'flatpages/post_detail.html'
    context_object_name = 'post'
