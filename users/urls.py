from django.urls import path
from. import views
from .views import SignUpView, Verifyview, ResendVerifyView


urlpatterns = [
     path('signup/',SignUpView.as_view()),
     path('verify/',Verifyview.as_view()),
     path('resend/',ResendVerifyView.as_view())
]