from django.conf import settings

PAGINATION = getattr(settings, "DJ_BOOKING_PAGINATION ", 10)
TEMUJANJI_BG = getattr(settings, 'TEMUJANJI_BG', 'img/booking_bg.jpg')
TEMUJANJI_DESC = getattr(settings, 'TEMUJANJI_DESC', 'jadikan temujanji lebih mudah dan cepat')
TEMUJANJI_TAJUK = getattr(settings, 'TEMUJANJI_TAJUK', 'Tempahan Temujanji')
TEMUJANJI_DISABLE_URL = getattr(settings, 'TEMUJANJI_DISABLE_URL', "/")
TEMUJANJI_SUCCESS_REDIRECT_URL =  getattr(settings, 'TEMUJANJI_SUCCESS_REDIRECT_URL', None)
