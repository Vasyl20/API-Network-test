from django.urls import path
from .views import NetworkTestView

urlpatterns = [
    path('network-test/', NetworkTestView.as_view(), name='network_test'),
]