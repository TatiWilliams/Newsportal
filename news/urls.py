from django.urls import path
from .views import AboutPageView, NewsPageView, PostDetailView, NewsSearchView, create_news, delete_news, \
    edit_news, create_article, delete_article, edit_article, PostCreate, PostEdit, PostDelete

urlpatterns = [
    path("", NewsPageView.as_view(), name="news"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="about"),

    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('news/create/', create_news, name='create_news'),
    path('news/<int:pk>/edit/', edit_news, name='edit_news'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('edit/', PostEdit.as_view(), name='post_edit'),
    path('delete/', PostDelete.as_view(), name='post_delete'),
    path('news/<int:pk>/delete/', delete_news, name='delete_news'),
    path('articles/create/', create_article, name='create_article'),
    path('articles/<int:pk>/edit/', edit_article, name='edit_article'),
    path('articles/<int:pk>/delete/', delete_article, name='delete_article'),
]
