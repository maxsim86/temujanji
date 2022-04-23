from django.db import models
from django.conf import settings

# Create your models here.

TEMPOH_BOOKING = (
    ("5", "5M"),
    ("10", "10M"),
    ("15", "15M"),
    ("20", "20M"),
    ("25", "25M"),
    ("30", "30M"),
    ("35", "35M"),
    ("40", "40M"),
    ("45", "45M"),
    ("60", "1H"),
    ("75", "1H 15M"),
    ("90", "1H 30M"),
    ("105", "1H 45M"),
    ("120", "2H"),
    ("150", "2H 30M"),
    ("180", "3H"),
)


class Tempahan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True
    )

    tarikh = models.DateField()
    masa = models.TimeField()
    nama_pengguna = models.CharField(max_length=250)
    email_pengguna = models.EmailField()
    approved = models.BooleanField(default=False)
    telefon_pengguna = models.CharField(blank=True, null=True, max_length=10)
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_ad = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user_name or "Tiada Nama"


class SettingTempahan(models.Model):
    # General
    tempahan_enable = models.BooleanField(default=True)
    pengesaan_diperlukan = models.BooleanField(
        default=True,
    )
    # Tarikh
    matikan_hujung_minggu = models.BooleanField(default=True)
    tempahan_available_sebulan = models.IntegerField(default=True)
    max_tempahan_per_hari = models.IntegerField(null=True, blank=True)

    # Masa
    masa_mula = models.TimeField()
    masa_tamat = models.TimeField()
    period_setiap_tempahan = models.CharField(
        max_length=200,
        default=30,
        choices=TEMPOH_BOOKING,
        help_text="Berapa lama setiap tempahan diambil",
    )
    max_tempahan_per_masa = models.IntegerField(
        default=1,
        help_text="Berapa banyak temujanji boleh tempah dalam setiap satu satu masa",
    )
