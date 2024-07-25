from django.urls import path
from .views import NewsList, NewsDetails, NewsSearch, NewsCreateView, NewsUpdateView, NewsDeleteView, upgrade_me, \
    CategoryListView, subscribe

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetails.as_view(), name='news_details'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('add/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit', NewsUpdateView.as_view(), name='news_update'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]