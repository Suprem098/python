from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.FloatField()
    photos = models.ImageField(upload_to='photos/')
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    table_no = models.CharField(max_length=10)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return self.status
