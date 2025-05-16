from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.articles, name="articles"),
    path("<int:article_id>/", views.article, name="article"),
    path("create/", views.create_article, name="create_article"),
    path("update/<int:article_id>/", views.update_article, name="update_article"),
    path("delete/<int:article_id>/", views.delete_article, name="delete_article"),
    path("category/<slug:category_slug>/", views.category, name="category"),
    path("search/", views.search, name="search"),
]

