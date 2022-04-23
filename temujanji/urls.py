from django.urls import path
from .views import (TempahanHomeView, TempahanListView, TempahanSettingView,TempahanDeleteView, TempahanApproveView,dapatkan_masa_available, CiptaTemujanjiWizardView)

#www.domain.com/list_tempahan
urlpatterns = [
    path('', CiptaTemujanjiWizardView.as_view(), name='create_booking'),
    path('admin', TempahanHomeView.as_view(), name="admin_dashboard"),
    path("admin/list", TempahanListView.as_view(), name="list_tempahan"),
    path('admin/settings', TempahanSettingView.as_view(), name='tempahan_tempahan'),
    path('admin/<pk>/delete', TempahanDeleteView.as_view(), name='delete_tempahan'),
    path('admin/<pk>/approve', TempahanApproveView.as_view(), name='approve_tempahan'),
    path('get-available-time', dapatkan_masa_available, name="dapatkan_masa_available"),

]
