from django.urls import path
from .views import TempahanHomeView, TempahanListView


urlpatterns = [
    path("admin", TempahanHomeView.as_view(), name="cipta_tempahan"),
    path("admin/list", TempahanListView.as_view(), name="list_tempahan"),
]
