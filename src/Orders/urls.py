from django.urls import path
from . import views

urlpatterns = [
    path('client-payment/', views.new_client_payment),
]
