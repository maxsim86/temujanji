import datetime
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, View
from temujanji.forms import (
    TempahanMasaForm,
    TempahanSettingsForm,
    TempahanTarikhForm,
    TempahanPlangganForm,
)
from temujanji.models import Tempahan, SettingTempahan
from temujanji.settings import (
    PAGINATION,
    TEMUJANJI_BG,
    TEMUJANJI_DESC,
    TEMUJANJI_TAJUK,
    TEMUJANJI_DISABLE_URL,
    TEMUJANJI_SUCCESS_REDIRECT_URL,
)
from django.shortcuts import get_object_or_404, redirect, reverse, render
from typing import Dict, List

from formtools.wizard.views import SessionWizardView

from temujanji.utils import BookingSettingMixin


# Create your views here.
#########
# Bahagian Admin
#########


class TempahanHomeView(BookingSettingMixin, TemplateView):
    model = Tempahan
    template_name = "temujanji/admin/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["last_bookings"] = Tempahan.objects.filter().order_by("tarikh", "masa")
        context["tempahan_menunggu"] = Tempahan.objects.filter(approved=False).order_by(
            "-tarikh", "masa"
        )[:10]
        return context


class TempahanListView(BookingSettingMixin, ListView):
    model = Tempahan
    template_name = "temujanji/admin/list_tempahan.html"
    paginate_by = PAGINATION


class TempahanSettingView(BookingSettingMixin, UpdateView):
    form_class = TempahanSettingsForm
    template_name = "temujanji/admin/tempahan_settings.html"

    def get_object(self):
        return SettingTempahan.objects.filter().first()

    def get_success_url(self):
        return reverse("tempahan_settings")


class TempahanDeleteView(BookingSettingMixin, DeleteView):
    model = Tempahan
    success_url = reverse_lazy("list_tempahan")
    queryset = Tempahan.objects.filter()


class TempahanApproveView(BookingSettingMixin, View):
    model = Tempahan
    success_url = reverse_lazy("list_tempahan")
    fields = ("approved",)

    def post(self, request, *args, **kwargs):
        tempahan = get_object_or_404(Tempahan, pk=self.kwargs.get("pk"))
        tempahan.approved = True
        tempahan.save()

        return redirect(self.success_url)

        #################
        # Part Untuk Book Temujanji
        #################


BOOK_STEP_FORMS = (
    ("Tarikh", TempahanTarikhForm),
    ("Masa", TempahanMasaForm),
    ("Info Pelanggan", TempahanPlangganForm),
)


class CiptaTemujanjiWizardView(SessionWizardView):
    template_name = "temujanji/user/booking_wizard.html"
    form_list = BOOK_STEP_FORMS

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        progress_width = "6"
        if self.steps.current == "Masa":
            context["dapatkan_masa_available"] = dapatkan_masa_available(
                self.get_cleaned_data_for_step("Tarikh")["tarikh"]
            )
            progress_width = "30"
        if self.steps.current == "Info Pelanggan":
            progress_width = "75"

        context.update(
            {
                "tempahan_settings": SettingTempahan.objects.first(),
                "progress_width": progress_width,
                "booking_bg": TEMUJANJI_BG,
                "description": TEMUJANJI_DESC,
                "title": TEMUJANJI_TAJUK,
            }
        )
        return context

    def render(self, form=None, **kwargs):
        # Check jika temujanji dimatikan/Disable
        form = form or self.get_form()
        context = self.get_context_data(form=form, **kwargs)

        if not context["tempahan_settings"].tempahan_enable:
            return redirect(TEMUJANJI_DISABLE_URL)

        return self.render_to_response(context)

    def done(self, form_list, **kwargs):
        data = dict(
            (key, value)
            for form in form_list
            for key, value in form.cleaned_data.items()
        )
        temujanji = Tempahan.objects.create(**data)

        if TEMUJANJI_SUCCESS_REDIRECT_URL:
            return redirect(TEMUJANJI_SUCCESS_REDIRECT_URL)

        return render(
            self.request,
            "temujanji/user/tempahan_done.html",
            {
                "progress_width": "100",
                "booking_id": temujanji.id,
                "booking_bg": TEMUJANJI_BG,
                "descriptions": TEMUJANJI_DESC,
                "title": TEMUJANJI_TAJUK,
            },
        )


def add_delta(masa: datetime.time, delta: datetime.datetime) -> datetime.time:
    # transform kepada full datetime first
    return (datetime.datetime.combine(datetime.date.today(), time) + delta).time()


def dapatkan_masa_available(date: datetime.date) -> List[Dict[datetime.time, bool]]:
    """
    Check semua availlable masa untuk pilih tarikh, masa mestilah antara masa_mula dan masa_tamat sekiranya masa sudah diambil -> is_taken = True

    """

    tempahan_settings = SettingTempahan.objects.first()
    tempahan_sediaada = Tempahan.objects.filter(tarikh=tarikh).values_list("masa")

    next_time = tempahan_settings.masa_mula
    time_list = []
    while True:
        is_taken = any([x[0] == next_time for x in tempahan_sediaada])
        time_list.append(
            {"time": ":".join(str(next_time).split(":")[:-1]), "is_taken": is_taken}
        )
        next_time = add_delta(
            next_time,
            datetime.timedelta(minutes=int(tempahan_settings.period_of_each_booking)),
        )
        if next_time > tempahan_settings.masa_tamat:
            break
    return time_list
