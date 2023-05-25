from django.urls import path

from dispatch.views import create_client, update_client, MailingStatsView

urlpatterns = [
    path('clients/', create_client, name='create_client'),
    path('clients/<int:pk>/', update_client, name='update_client'),
    path('stats/', MailingStatsView.as_view(), name='mailing_stats'),
]
