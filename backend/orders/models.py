from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Ürün Adı")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Fiyat")
    category = models.CharField(max_length=100, verbose_name="Kategori")
    image_url = models.URLField(blank=True, null=True, verbose_name="Resim URL")
    stock = models.IntegerField(default=0, verbose_name="Stok")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Ürün"
        verbose_name_plural = "Ürünler"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('processing', 'İşleniyor'),
        ('shipped', 'Kargolandı'),
        ('delivered', 'Teslim Edildi'),
        ('cancelled', 'İptal Edildi'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField(default=1, verbose_name="Adet")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Durum")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Sipariş Tarihi")

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.date})"

    class Meta:
        verbose_name = "Sipariş"
        verbose_name_plural = "Siparişler"