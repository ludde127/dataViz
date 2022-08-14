from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="social_index"),
    path("block/<str:hid>", views.block, name="block"),
    path("content/<int:id>", views.content, name="content"),
    path("delete-content/<int:id>", views.delete_content, name="delete_content"),
    path("add-block", views.add_block, name="add_block"),
    path("add-top-content/<int:block_id>", views.add_top_content, name="add_top_content"),
    path("modify/<int:id>/<int:is_block>", views.modify, name="modify")

]