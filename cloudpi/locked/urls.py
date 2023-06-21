from django.urls import path
from .views import LockedSendOTPView, LockedVerifyOTPView
from . import views

urlpatterns = [
    path('send-otp/', LockedSendOTPView.as_view(), name='locked-send-otp'),
    path('verify-otp/', LockedVerifyOTPView.as_view(), name='locked-verify-otp'),
]