from django.urls import path
from .views import EventAPIView
from . import views

urlpatterns = [
    path('api/events', EventAPIView.as_view(), name='event-api'),
    path('statistics/', views.event_statistics, name='event_statistics'),
    path('successes/', views.payment_success, name='payment_success'),
]
