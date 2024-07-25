from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView)
from .filters import PostFilter
from .forms import NewsForm
from django.views import generic

from django.views.decorators.csrf import csrf_protect
from .models import Post, Category


class NewsList(ListView):
    model = Post
    ordering = '-date'
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 5


class NewsDetails(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/news_details.html'
    context_object_name = 'news_post'


class NewsSearch(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class NewsCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    template_name = 'news/news_create.html'
    form_class = NewsForm


class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    template_name = 'news/news_create.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return get_object_or_404(Post, pk=id)


class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
@csrf_protect
def subscribe(request, pk):
    user = request.user
    category = get_object_or_404(Category, id=pk)
    category.subscribers.add(user)
    message = 'Вы успешно подписались на рассылку новостей'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})


class PostEdit(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = NewsForm
    template_name = 'flatpages/edit_news.html'
    success_url = reverse_lazy('news_list')

    def get_success_url(self):
        post = self.get_object()
        if post.post_type == 'NW':
            return reverse_lazy('news_detail', kwargs={'pk': post.pk})
        elif post.post_type == 'AR':
            return reverse_lazy('article_detail', kwargs={'pk': post.pk})
        return super().get_success_url()


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/delete_news.html'
    success_url = reverse_lazy('news_list')

    def get_success_url(self):
        post = self.get_object()
        if post.post_type == 'NW':
            return reverse_lazy('news_list')
        elif post.post_type == 'AR':
            return reverse_lazy('article_list')
        return super().get_success_url()


class HomePageView(TemplateView):
    template_name = "flatpages/home.html"


class AboutPageView(TemplateView):
    template_name = "flatpages/about.html"


class NewsPageView(ListView):
    model = Post
    ordering = '-date'
    template_name = "flatpages/news.html"
    context_object_name = 'news'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_list = context['news']
        for news in news_list:
            news.text = news.text[:20]
        return context


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'post'


class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'flatpages/edit_news.html'


def upgrade_me(request):
    user = request.user
    premium_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        premium_group.user_set.add(user)
    return redirect('/news')


class CategoryListView(NewsList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
