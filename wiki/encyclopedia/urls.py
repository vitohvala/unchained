from django.urls import path

from . import views

app_name = "wikis"

urlpatterns = [
    path("", views.index, name="index"),
    path("rand", views.rendoom, name="rendoom"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("new/", views.new_page, name="new_p"),
    path("search/", views.search, name="search"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit")
]
