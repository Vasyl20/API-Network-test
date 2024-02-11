from django.urls import path
from .views import NetworkTestView, LastTestResultsView 

urlpatterns = [
    path('network-test/', NetworkTestView.as_view(), name='network_test'),
    path('last-test-results/', LastTestResultsView.as_view(), name='last-test-results'),
]