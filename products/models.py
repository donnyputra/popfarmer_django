from django.db import models

class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Product(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    unit_of_measure = models.ForeignKey(UnitOfMeasure, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name