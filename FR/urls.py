from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from dispatch.views import DispatchViewSet, ClientViewSet, MailingViewSet

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailings', MailingViewSet)
router.register(r'dispatches', DispatchViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include(router.urls)),
    path('dispatch/', include('dispatch.urls')),
]
