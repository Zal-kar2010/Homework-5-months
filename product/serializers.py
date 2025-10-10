from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Count, Avg

# --- Базовые Сериализаторы для CRUD операций ---

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_id']

class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    
    # КРИТИЧЕСКОЕ ИЗМЕНЕНИЕ: УДАЛЕНО read_only=True для stars
    # Теперь stars может быть передано в POST/PUT/PATCH запросах.
    # Валидация (MinValueValidator/MaxValueValidator) будет применяться автоматически моделью.
    stars = serializers.IntegerField() 
    # В качестве альтернативы, можно было бы просто удалить эту строку, 
    # так как stars автоматически включается в fields ниже.

    class Meta:
        model = Review
        # Включаем stars в fields, чтобы обеспечить его запись и чтение.
        fields = ['id', 'text', 'stars', 'product', 'product_id']

# ----------------------------------------------------------------------
## --- Сериализаторы для выполнения Домашнего Задания ---

# Эти сериализаторы не требуют изменений, так как они используются только для чтения (GET) данных.

# 1. Сериализатор для вложенных отзывов с полем stars
class NestedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']

# 2. Сериализатор для товаров с рейтингом и отзывами (Эндпоинт: /products/reviews/)
class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = NestedReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'rating', 'reviews']
    
    def get_rating(self, product):
        if hasattr(product, 'rating') and product.rating is not None:
            return round(product.rating, 2)
        return 0.0

# 3. Сериализатор для категорий с количеством товаров (Эндпоинт: /categories/)
class CategoryProductCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count'] 
    
    def get_products_count(self, category):
        if hasattr(category, 'products_count'):
            return category.products_count
        return 0