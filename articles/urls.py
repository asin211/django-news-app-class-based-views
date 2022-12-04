from django.urls import path

from .views import (
    HomePageView,
    ArticleListView,
    ArticleDetailView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleCreateView,  # new
)

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="article_edit"),
    path("<int:pk>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("new/", ArticleCreateView.as_view(), name="article_new"),  # new
    path("articles/", ArticleListView.as_view(), name="article_list"),
]
