from django.contrib import admin
from temujanji.models import Tempahan, SettingTempahan

# Register your models here.
@admin.register(Tempahan)
class AdminTempahan(admin.ModelAdmin):
    list_display = (
        "email_pengguna",
        "nama_pengguna",
        "tarikh",
        "masa",
        "approved",
    )
    list_filter = ("approved", "tarikh")
    ordering = ("tarikh", "masa")
    search_fields = ("email_pengguna", "nama_pengguna")


admin.site.register(SettingTempahan)
