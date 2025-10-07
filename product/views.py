from rest_framework import generics
from django.db.models import Count, Avg  # Импортируем Count и Avg для агрегации
from .models import Category, Product, Review
from .serializers import (
    CategoryProductCountSerializer,  # Новый сериализатор для категорий с количеством
    ProductReviewsSerializer,        # Новый сериализатор для товаров с рейтингом
    CategorySerializer, 
    ProductSerializer, 
    ReviewSerializer
)


# Categories
# Новый класс для эндпоинта /api/v1/categories/ с количеством товаров
class CategoryProductCountListView(generics.ListAPIView):
    # Используем аннотирование (Count) для подсчета товаров в каждой категории
    queryset = Category.objects.annotate(products_count=Count('products'))
    serializer_class = CategoryProductCountSerializer


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# Products
# Новый класс для эндпоинта /api/v1/products/reviews/ со средним баллом
class ProductReviewsListView(generics.ListAPIView):
    # Используем аннотирование (Avg) для вычисления среднего балла (stars)
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductReviewsSerializer


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Products (Оставляем старый, если он нужен для отдельного URL без рейтингов)
class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Reviews
class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer