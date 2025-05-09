from django.db import models
from django.utils.text import slugify 
import qrcode
from qr_cafe.settings import SITE_DOMAIN, MEDIA_ROOT


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photos = models.ImageField(upload_to='photos/')
    available = models.BooleanField(default=True)
    cafe=models.ForeignKey("CafeModel", on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.name


class CafeModel(models.Model):
    cafeid=models.SlugField(max_length=500, blank=True, unique=True)
    name=models.CharField(max_length=200)
    address=models.CharField(max_length=200)
    contact=models.CharField(max_length=100)
    logo=models.ImageField(upload_to="photos/")
    qr=models.ImageField(upload_to="qr", blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.cafeid:
            self.cafeid = slugify(self.name)
        url = f"http://{SITE_DOMAIN}/menu/{self.cafeid}"
        try:
            qr_image = qrcode.make(url)
            qr_image.save(f"{MEDIA_ROOT}/qr/{self.cafeid}.png")
            self.qr = f"qr/{self.cafeid}.png"
        except Exception as e:
            # Log error or handle accordingly
            print(f"Error generating QR code: {e}")
        super(CafeModel, self).save(*args, **kwargs)
    
    

class Order(models.Model):
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('mobile', 'Mobile Payment'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    table_no = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.status


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.name} ({self.email})"

class ContactSubmission(models.Model):
    cafe_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ContactSubmission from {self.cafe_name} by {self.contact_person}"
