from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("plot/<str:key>", views.plot, name="plot"),
    path("view-secret-key/<str:public_key>", views.secrets_for_data_store, name="secret_key"),
    path("plot/modify-data/<str:key>", views.modify_datastore, name="modify_data"),
    path("plot/modify-plot/<int:id>", views.modify_plot, name="modify_plot"),
    path("datastore/delete/<str:key>", views.delete_datastore, name="delete_datastore"),
    path("plot/create-all-can-view-url/<str:key>", views.get_all_can_view_link, name="plot_all_can_view"),
    path("plot/<str:key>/<str:all_can_view_key>", views.plot_all_can_view, name="all_can_view")
]