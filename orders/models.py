import uuid
from django.db import models
from django.utils import timezone
from suppliers.models import Supplier  # Import the Supplier model


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('in_delivery', 'In Delivery'),
        ('received_and_waiting_for_payment', 'Received & Waiting for Payment'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    def generate_order_code():
        today = timezone.now().strftime('%Y%m%d')
        last_order = Order.objects.order_by('-id').first()
        last_order_id = last_order.id if last_order else 0
        return f'{today}-{last_order_id + 1:05d}'
    
    # order_code = models.CharField(max_length=100)
    # order_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order_code = models.CharField(max_length=20, default=generate_order_code, editable=False)
    delivery_date = models.DateField()
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    store = models.ForeignKey('customers.Store', on_delete=models.CASCADE)
    # Add other fields as needed

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    requested_qty = models.IntegerField(null=True, blank=True)
    fulfilled_qty = models.IntegerField(null=True, blank=True)
    received_qty = models.IntegerField(null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    # Add other fields as needed

class OrderRequestSummary(models.Model):
    delivery_date = models.DateField()
    product_name = models.CharField(max_length=100)
    total_requested_qty = models.IntegerField()

    class Meta:
        # Specify that this model is for viewing only
        managed = False
        db_table = "order_request_summary_view"
        # Optionally, provide a descriptive name for the model in the admin interface
        verbose_name = "Order Request Summary"
        verbose_name_plural = "Order Request Summaries"

    # def __str__(self):
    #     return f"OrderRequestSummary - Delivery Date: {self.delivery_date}, Product Name: {self.product_name}, Requested Qty: {self.requested_qty}"

    # @classmethod
    # def get_summary_data(cls):
    #     summary_data = []
    #     # Aggregate order items based on delivery_date
    #     order_items_aggregated = OrderItem.objects.values('order__delivery_date', 'product__product_name').annotate(total_requested_qty=models.Sum('requested_qty'))
    #     # Convert aggregated data to OrderRequestSummary objects
    #     for item in order_items_aggregated:
    #         summary_data.append(cls(
    #             delivery_date=item['order__delivery_date'],
    #             product_name=item['product__product_name'],
    #             requested_qty=item['total_requested_qty']
    #         ))
    #     return summary_data
