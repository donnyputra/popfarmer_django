# Generated by Django 5.0.4 on 2024-04-14 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_orderrequestsummary_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='rejected_qty',
        ),
    ]
