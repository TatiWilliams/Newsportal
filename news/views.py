from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView, TemplateView, CreateView, UpdateView, DeleteView, DetailView)
from django.views import generic
from .models import Post
from .filters import PostFilter
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm


def create_news(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.categoryType = 'NW'
            post.save()
            return redirect('news_list')
    else:
        form = PostForm()
    return render(request, 'flatpages/create_news.html', {'form': form})


def delete_news(request, pk):
    news = get_object_or_404(Post, pk=pk, categoryType='NW')
    if request.method == 'POST':
        news.delete()
        return redirect('news_list')
    return render(request, 'flatpages/delete_news.html', {'news': news})


def edit_news(request, pk):
    news = get_object_or_404(Post, pk=pk, categoryType='NW')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = PostForm(instance=news)
    return render(request, 'flatpages/edit_news.html', {'form': form})


def create_article(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.categoryType = 'AR'
            post.save()
            return redirect('article_list')
    else:
        form = PostForm()
    return render(request, 'flatpages/create_article.html', {'form': form})


def delete_article(request, pk):
    article = get_object_or_404(Post, pk=pk, categoryType='AR')
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'flatpages/delete_article.html', {'news': article})


def edit_article(request, pk):
    article = get_object_or_404(Post, pk=pk, categoryType='AR')
    if request.method == 'POST':
        form = PostForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = PostForm(instance=article)
    return render(request, 'flatpages/edit_article.html', {'form': form})


class PostEdit(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'flatpages/edit_news.html'
    success_url = reverse_lazy('news_list')

    def get_success_url(self):
        post = self.get_object()
        if post.categoryType == 'NW':
            return reverse_lazy('news_detail', kwargs={'pk': post.pk})
        elif post.categoryType == 'AR':
            return reverse_lazy('article_detail', kwargs={'pk': post.pk})
        return super().get_success_url()


class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/delete_news.html'
    success_url = reverse_lazy('news_list')

    def get_success_url(self):
        post = self.get_object()
        if post.categoryType == 'NW':
            return reverse_lazy('news_list')
        elif post.categoryType == 'AR':
            return reverse_lazy('article_list')
        return super().get_success_url()


# Existing class-based views

class HomePageView(TemplateView):
    template_name = "flatpages/home.html"


class AboutPageView(TemplateView):
    template_name = "flatpages/about.html"


class NewsPageView(ListView):
    model = Post
    ordering = '-dateCreation'
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


class NewsSearchView(ListView):
    model = Post
    template_name = 'flatpages/news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10
    filterset = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'flatpages/edit_news.html'
