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
    # Добавляем поле stars
    stars = serializers.IntegerField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product', 'product_id']

# ----------------------------------------------------------------------
## --- Сериализаторы для выполнения Домашнего Задания ---

# 1. Сериализатор для вложенных отзывов с полем stars
class NestedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']

# 2. Сериализатор для товаров с рейтингом и отзывами (Эндпоинт: /products/reviews/)
class ProductReviewsSerializer(serializers.ModelSerializer):
    # Вложенные отзывы (используем related_name="reviews" из модели)
    reviews = NestedReviewSerializer(many=True, read_only=True)
    
    # Вычисляемое поле для среднего балла
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'rating', 'reviews']
    
    def get_rating(self, product):
        # Получаем значение `rating`, аннотированное во View, и округляем его
        if hasattr(product, 'rating') and product.rating is not None:
            return round(product.rating, 2)
        return 0.0

# 3. Сериализатор для категорий с количеством товаров (Эндпоинт: /categories/)
class CategoryProductCountSerializer(serializers.ModelSerializer):
    # Вычисляемое поле для количества товаров
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count'] 
    
    def get_products_count(self, category):
        # Получаем значение `products_count`, аннотированное во View
        if hasattr(category, 'products_count'):
            return category.products_count
        return 0