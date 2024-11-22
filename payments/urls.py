# payments/urls.py
from django.urls import path
from . import views

app_name = 'payments'  # This defines the namespace

urlpatterns = [
    path('initiate/<int:project_id>/', views.initiate_payment, name='initiate_payment'),
    path('verify/', views.verify_payment, name='verify_payment'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('history/', views.payment_history, name='payment_history'),
]