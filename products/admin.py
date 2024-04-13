from django.contrib import admin
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import UnitOfMeasure, Product

admin.site.register(UnitOfMeasure)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'get_unit_of_measure_name', 'format_unit_price', 'format_supplier_price')
    search_fields = ['code', 'name', 'unit_of_measure__name']  # Define fields to search
    list_filter = ['unit_of_measure']  # Enable filter for unit_of_measure field
    list_per_page = 10

    def get_unit_of_measure_name(self, obj):
        return obj.unit_of_measure.name

    get_unit_of_measure_name.short_description = 'Unit of Measure'

    def format_unit_price(self, obj):
        return 'Rp {}'.format(intcomma(obj.unit_price))

    format_unit_price.short_description = 'Unit Price (IDR)'

    def format_supplier_price(self, obj):
        return 'Rp {}'.format(intcomma(obj.supplier_price))

    format_supplier_price.short_description = 'Supplier Price (IDR)'