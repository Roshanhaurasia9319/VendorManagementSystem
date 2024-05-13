from rest_framework import serializers
from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance

class VendorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Vendor
        fields="__all__"
        
class POSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=PurchaseOrder
        fields="__all__"
        
class HPSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=HistoricalPerformance
        fields="__all__"