# Generated by Django 5.0.4 on 2024-04-13 15:16

import django.db.models.deletion
import orders.models
from django.db import migrations, models

SQL_CREATE_VIEW = """
CREATE VIEW order_request_summary_view AS
SELECT
    ROW_NUMBER() OVER () AS id,
    o.delivery_date,
    p.name AS product_name,
    SUM(oi.requested_qty) AS total_requested_qty
FROM
    orders_orderitem oi
JOIN
    orders_order o ON oi.order_id = o.id
JOIN
    products_product p ON oi.product_id = p.id
GROUP BY
    o.delivery_date, p.name;
"""

SQL_DROP_TABLE = """
DROP TABLE IF EXISTS orders_requestedqtysummary;
"""

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0001_initial'),
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_code', models.CharField(default=orders.models.Order.generate_order_code, editable=False, max_length=20)),
                ('delivery_date', models.DateField()),
                ('order_status', models.CharField(choices=[('new', 'New'), ('in_progress', 'In Progress'), ('in_delivery', 'In Delivery'), ('received_and_waiting_for_payment', 'Received & Waiting for Payment'), ('completed', 'Completed'), ('canceled', 'Canceled')], max_length=50)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customers.store')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_qty', models.IntegerField(blank=True, null=True)),
                ('fulfilled_qty', models.IntegerField(blank=True, null=True)),
                ('received_qty', models.IntegerField(blank=True, null=True)),
                ('rejected_qty', models.IntegerField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='orders.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='OrderRequestSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_date', models.DateField()),
                ('product_name', models.CharField(max_length=100)),
                ('total_requested_qty', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Order Request Summary',
                'verbose_name_plural': 'Order Request Summaries',
                'managed': False,
            },
        ),
        migrations.RunSQL(SQL_CREATE_VIEW),
        migrations.RunSQL(SQL_DROP_TABLE),
    ]
