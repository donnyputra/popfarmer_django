from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils.html import format_html
# from daterangefilter.filters import DateRangeFilter
from django.utils.translation import gettext_lazy as _
import sys
from .models import Order, OrderItem, OrderRequestSummary

def process_order(modeladmin, request, queryset):
    for order in queryset:
        if order.order_status != "in_progress":
            queryset.update(order_status="in_progress")

process_order.short_description = _("Process Order")


def deliver_order(modeladmin, request, queryset):
    for order in queryset:
        if order.order_status != "in_delivery":
            queryset.update(order_status="in_delivery")

deliver_order.short_description = _("Deliver Order")

def received_order(modeladmin, request, queryset):
    for order in queryset:
        if order.order_status != "received_and_waiting_for_payment":
            queryset.update(order_status="received_and_waiting_for_payment")

received_order.short_description = _("Mark Order as Received")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
            'order_code', 
            'formatted_delivery_date', 
            'display_order_status', 
            'store', 
            'total_ordered_price', 
            'total_fulfilled_price',
            'total_received_price',
            # 'total_supplier_price',
            # 'profit_loss'
        )
    inlines = [OrderItemInline]
    search_fields = ['order_code', 'store__name', 'delivery_date']
    list_filter = ['order_status', 'store', ('delivery_date', admin.DateFieldListFilter)]

    actions = [ process_order, deliver_order, received_order ]

    def formatted_delivery_date(self, obj):
        return obj.delivery_date.strftime('%Y-%m-%d')

    formatted_delivery_date.short_description = 'Delivery Date (YYYY-MM-DD)'

    def display_order_status(self, obj):
        status = obj.get_order_status_display()
        color_map = {
            'New': 'primary',
            'In Progress': 'info',
            'In Delivery': 'warning',
            'Received & Waiting for Payment': 'secondary',
            'Completed': 'success',
        }
        badge_color = color_map.get(obj.get_order_status_display(), 'dark')
        return format_html('<span class="badge badge-{0}">{1}</span>', badge_color, status)

    display_order_status.short_description = 'Order Status'

    def total_ordered_price(self, obj):
        total_price = sum(item.product.unit_price * item.requested_qty for item in obj.order_items.all())
        return 'Rp {}'.format(intcomma(total_price))

    total_ordered_price.short_description = 'Total Ordered Price'

    def total_fulfilled_price(self, obj):
        total_price = sum(item.product.unit_price * (item.fulfilled_qty if item.fulfilled_qty is not None else 0) for item in obj.order_items.all())
        return 'Rp {}'.format(intcomma(total_price))

    total_fulfilled_price.short_description = 'Total Fulfilled Price'

    def total_received_price(self, obj):
        total_price = sum(item.product.unit_price * (item.received_qty if item.received_qty is not None else 0) for item in obj.order_items.all())
        return 'Rp {}'.format(intcomma(total_price))

    total_received_price.short_description = 'Total Received Price'

    # def total_supplier_price(self, obj):
    #     total_price = sum(item.product.supplier_price * (item.fulfilled_qty if item.fulfilled_qty is not None else 0) for item in obj.order_items.all())
    #     return 'Rp {}'.format(intcomma(total_price))

    # total_supplier_price.short_description = 'Total Supplier Price'

    # def profit_loss(self, obj):
    #     total_unit_price = sum(item.product.unit_price * item.requested_qty for item in obj.order_items.all())
    #     total_supplier_price = sum(item.product.supplier_price * item.requested_qty for item in obj.order_items.all())
    #     profit_loss = total_unit_price - total_supplier_price
    #     return 'Rp {}'.format(intcomma(profit_loss))

    # profit_loss.short_description = 'Profit/Loss'



class OrderRequestSummaryAdmin(admin.ModelAdmin):
    list_display = ('formatted_delivery_date', 'product_name', 'total_requested_qty')
    search_fields = ['delivery_date', 'product_name']
    list_filter = ['delivery_date']

    def formatted_delivery_date(self, obj):
        return obj.delivery_date.strftime('%Y-%m-%d')

    formatted_delivery_date.short_description = 'Delivery Date (YYYY-MM-DD)'

    def has_add_permission(self, request):
        # Disable the "Add" button in the admin interface
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the "Change" button in the admin interface
        return False

    def has_delete_permission(self, request, obj=None):
        # Disable the "Delete" button in the admin interface
        return False

    class Meta:
        verbose_name = "Order Request Summary"
        verbose_name_plural = "Order Request Summaries"

admin.site.register(OrderRequestSummary, OrderRequestSummaryAdmin)