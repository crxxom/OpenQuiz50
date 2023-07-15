from django.urls import path

from . import views

urlpatterns = [
path("", views.home, name="home"),
path("create/", views.create, name="create"),
path("play/", views.play, name="play"),
path("play/room/<str:room_id>", views.room, name="room"),
path("questionbank/<str:category>", views.questionbank, name="questionbank"),
path("search/", views.search_result, name="search_result")
# path("admin_db_mod/", views.add_db, name="add_db")
]