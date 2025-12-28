from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name_ru = models.CharField(max_length=200)
    name_uz = models.CharField(max_length=200)

    def __str__(self):
        return self.name_ru

    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    name_ru = models.TextField()
    name_uz = models.TextField()
    description_ru = models.TextField(blank=True, null=True)
    description_uz = models.TextField(blank=True, null=True)
    price = models.CharField(max_length=100)  # Теперь varchar(100), для "100 000 сум" или диапазона
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    photo_path = models.CharField(max_length=255, blank=True, null=True)  # Оставил как в вашем SQL, если нужно legacy

    def __str__(self):
        return self.name_ru

    def clean(self):
        # Валидация: минимум одно изображение
        if not self.images.exists():
            raise ValidationError('Продукт должен иметь хотя бы одно изображение.')

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(upload_to='product_images/')  # Используем ImageField для загрузки файлов
    image_alt_ru = models.CharField(max_length=200, blank=True, null=True)
    image_alt_uz = models.CharField(max_length=200, blank=True, null=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=['product', 'sort_order'])]
        ordering = ['sort_order']

    def __str__(self):
        return f"Image for {self.product.name_ru}"