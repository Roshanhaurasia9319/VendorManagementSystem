from django.contrib import admin
from django.urls import path,include
from vendor.views import VendorViewSet, POViewSet, HPViewSet
from rest_framework import routers
from .import views


router = routers.DefaultRouter()
router.register(r'Vendor', VendorViewSet)
router.register(r'PurchaseOrder', POViewSet)
router.register(r'HistoricalPerformance', HPViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('index/', views.index, name="index")
]