from django.shortcuts import render
from rest_framework import viewsets
from vendor.models import Vendor, PurchaseOrder, HistoricalPerformance
from vendor.serializers import VendorSerializer, POSerializer, HPSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class VendorViewSet(viewsets.ModelViewSet):
    queryset=Vendor.objects.all()
    serializer_class=VendorSerializer
    @action(detail=True, methods=['get'])
    def purchase_order(self, request, pk=None):
        try:
            vendor = self.get_object()
            po=PurchaseOrder.objects.filter(vendor=vendor)
            po_serializer = POSerializer(po, many=True, context={'request':request})
            return Response(po_serializer.data)
        except Exception as e:
            print(e)
            return Response({
                'message':"Data may not be exist !! Error"
            })
    
    
class POViewSet(viewsets.ModelViewSet):
    queryset=PurchaseOrder.objects.all()
    serializer_class=POSerializer
    
class HPViewSet(viewsets.ModelViewSet):
    queryset=HistoricalPerformance.objects.all()
    serializer_class=HPSerializer


def index(request):
    return render(request, "index.html")