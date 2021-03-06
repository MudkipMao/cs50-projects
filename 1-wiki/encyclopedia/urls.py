from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("random/", views.random, name="random"),
    path("wiki/<str:article_name>", views.article, name="article"),
    path("search", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit", views.edit, name="edit")
]
