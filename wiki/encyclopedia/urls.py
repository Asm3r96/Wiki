from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/<str:title>', views.entry, name="entry"),
    path("editPage",views.editPage, name='editPage'),
    path("search", views.search, name="search"),
]
