from django.contrib import admin
from .models import Category, Product, ProductImage

class ProductImageInline(admin.TabularInline):  # Для inline редактирования изображений в продукте
    model = ProductImage
    extra = 1  # По умолчанию показывает 1 пустую форму для добавления
    fields = ('image_url', 'image_alt_ru', 'image_alt_uz', 'sort_order')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'name_uz')
    search_fields = ('name_ru', 'name_uz')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'category', 'price')
    search_fields = ('name_ru', 'name_uz')
    list_filter = ('category',)
    fields = ('name_ru', 'name_uz', 'description_ru', 'description_uz', 'price', 'category', 'photo_path')
    inlines = [ProductImageInline]  # Изображения inline под продуктом
    autocomplete_fields = ['category']  # Поиск по категориям

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):  # Отдельная админка для изображений, если нужно
    list_display = ('product', 'sort_order')
    list_filter = ('product',)