from django.urls import path

from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path("search-suggestions/", search_suggestions, name="search_suggestions"),
    path('article/detail/<slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article/like/<slug>/', ArticleLikeView.as_view(), name='article_like'),
    path('articles/new/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<slug>/edit/', ArticleEditView.as_view(), name='article_update'),
    path("article/<slug>/delete/", ArticleDeleteView.as_view(), name="article_delete"),
    path("comment/<slug>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
    path('category/<slug>/', CategoryArticleListView.as_view(), name='category_article_list'),
]
