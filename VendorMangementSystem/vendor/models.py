from django.db import models
from django.db.models import Count, F, ExpressionWrapper, DecimalField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import timezone, timedelta
from django.db.models import Avg



# Create your models here.
class Vendor(models.Model):
    name=models.CharField(max_length=50)
    contact_details=models.TextField()
    address=models.TimeField(auto_now=True)
    vendor_code=models.CharField(max_length=50)
    on_time_delivery_rate=models.FloatField(null=True)
    quality_rating_avg=models.FloatField(null=True)
    average_response_time=models.FloatField(null=True)
    fulfillment_rate=models.FloatField(null=True)
    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    po_number=models.CharField(max_length=50)
    vendor=models.ForeignKey("Vendor", on_delete=models.CASCADE)
    order_date=models.DateTimeField(auto_now=True)
    delivery_date=models.DateTimeField(auto_now=True)
    item=models.CharField(max_length=50)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=100, choices=(("Pending","Pending"),("Completed","Completed")))
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True)
    def __str__(self):
        return self.vendor
    
    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)
    def __str__(self):
        return self.vendor
    
    
    
    
def update_on_time_delivery_rate(sender, instance, **kwargs):
    if instance.status == 'completed':
        completed_po_count = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').count()
        on_time_po_count = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed', delivery_date__lte=F('acknowledgment_date')).count()
        on_time_delivery_rate = (on_time_po_count / completed_po_count) if completed_po_count != 0 else 0
        
        # Update the on_time_delivery_rate field of the Vendor
        Vendor.objects.filter(pk=instance.vendor.pk).update(on_time_delivery_rate=on_time_delivery_rate)
        


# Update on-time delivery rate when a purchase order is saved
@receiver(post_save, sender=PurchaseOrder)
def update_metrics(sender, instance, **kwargs):
    if instance.status == 'completed':
        # Quality Rating Average
        completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed').exclude(quality_rating=None)
        quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
        instance.vendor.quality_rating_avg = quality_rating_avg
        instance.vendor.save()

        # Average Response Time
        completed_pos = PurchaseOrder.objects.filter(vendor=instance.vendor, status='completed', acknowledgment_date__isnull=False)
        response_times = [po.acknowledgment_date - po.issue_date for po in completed_pos]
        avg_response_time = sum(response_times, timedelta()) / len(response_times)
        instance.vendor.average_response_time = avg_response_time
        instance.vendor.save()

    # Fulfillment Rate
    total_pos = PurchaseOrder.objects.filter(vendor=instance.vendor)
    successful_pos = total_pos.filter(status='completed', issue_date__lte=F('acknowledgment_date'))
    fulfillment_rate = successful_pos.count() / total_pos.count() if total_pos.count() != 0 else 0
    instance.vendor.fulfillment_rate = fulfillment_rate
    instance.vendor.save()
