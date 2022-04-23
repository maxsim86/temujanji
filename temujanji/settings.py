from django.conf import settings

PAGINATION = getattr(settings, "DJ_BOOKING_PAGINATION ", 10)
