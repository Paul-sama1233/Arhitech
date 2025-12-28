from rest_framework import serializers
from .models import Category, Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # Извлекаем lang из контекста (будет передан из view)
        self.lang = kwargs.pop('lang', 'ru')  # По умолчанию 'ru'
        super().__init__(*args, **kwargs)

        # Динамически выбираем поля на основе lang
        if self.lang == 'uz':
            self.fields['name'] = serializers.CharField(source='name_uz')
        else:
            self.fields['name'] = serializers.CharField(source='name_ru')

        # Удаляем оригинальные _ru/_uz поля, чтобы возвращать только 'name'
        self.fields.pop('name_ru', None)
        self.fields.pop('name_uz', None)

    class Meta:
        model = Category
        fields = ['id', 'name_ru', 'name_uz']  # Базовые поля, будут модифицированы в __init__

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # Оставляем как есть, но передадим lang ниже
    images = ProductImageSerializer(many=True, read_only=True)

    def __init__(self, *args, **kwargs):
        self.lang = kwargs.pop('lang', 'ru')
        super().__init__(*args, **kwargs)

        # Динамически выбираем поля
        if self.lang == 'uz':
            self.fields['name'] = serializers.CharField(source='name_uz')
            self.fields['description'] = serializers.CharField(source='description_uz', allow_blank=True)
        else:
            self.fields['name'] = serializers.CharField(source='name_ru')
            self.fields['description'] = serializers.CharField(source='description_ru', allow_blank=True)

        # Удаляем _ru/_uz
        self.fields.pop('name_ru', None)
        self.fields.pop('name_uz', None)
        self.fields.pop('description_ru', None)
        self.fields.pop('description_uz', None)

        # Для изображений: динамически выбираем alt
        if self.lang == 'uz':
            self.fields['images'].child.fields['image_alt'] = serializers.CharField(source='image_alt_uz', allow_blank=True)
        else:
            self.fields['images'].child.fields['image_alt'] = serializers.CharField(source='image_alt_ru', allow_blank=True)
        self.fields['images'].child.fields.pop('image_alt_ru', None)
        self.fields['images'].child.fields.pop('image_alt_uz', None)

    def get_category(self, obj):
        # Передаём lang в CategorySerializer
        return CategorySerializer(obj.category, lang=self.lang).data

    class Meta:
        model = Product
        fields = ['id', 'name_ru', 'name_uz', 'description_ru', 'description_uz', 'price', 'category', 'photo_path', 'images']