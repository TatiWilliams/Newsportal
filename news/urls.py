from django.urls import path
from .views import HomePageView, AboutPageView, NewsPageView, PostDetailView



urlpatterns = [
    path("", NewsPageView.as_view(), name="news"),
    path("<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("about/", AboutPageView.as_view(), name="about"),
    path("", HomePageView.as_view(), name="home"),
]



