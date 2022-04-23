import datetime
from django.views.generic import TemplateView, ListView
from django.shortcuts import render
from temujanji.models import Tempahan, SettingTempahan
from temujanji.settings import PAGINATION


# Create your views here.
#########
# Bahagian Admin
#########


class TempahanHomeView(TemplateView):
    model = Tempahan
    template_name = "tempahan/admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_bookings"] = Tempahan.objects.filter().order_by("tarikh", "masa")
        context["tempahan_menunggu"] = Tempahan.objects.filter(approved=False).order_by(
            "-tarikh", "masa"
        )[:10]
        return context


class TempahanListView(ListView):
    model = Tempahan
    template_name = "tempahan/admin/list_tempahan.html"
    paginate_by = PAGINATION
