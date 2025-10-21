from rest_framework import generics, status
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Category, Product, Review
from .serializers import (
    CategoryProductCountSerializer,
    ProductReviewsSerializer,
    CategorySerializer,
    ProductSerializer,
    ReviewSerializer
)


# -----------------------------------------------------------
# CATEGORIES
# -----------------------------------------------------------

# /api/v1/categories/
class CategoryListCreateView(generics.ListCreateAPIView):
    """
    Получение списка категорий с подсчётом товаров (GET)
    и создание новой категории (POST).
    """
    def get_queryset(self):
        # Подсчёт количества товаров в каждой категории
        return Category.objects.annotate(products_count=Count('products'))

    def get_serializer_class(self):
        # Используем разный сериализатор для GET и POST
        if self.request.method == 'GET':
            return CategoryProductCountSerializer
        return CategorySerializer
    
    # Метод create не переопределяем, так как стандартная логика DRF
    # (валидация -> perform_create -> 201 Response) подходит.


# /api/v1/categories/<int:pk>/
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление конкретной категории.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -----------------------------------------------------------
# PRODUCTS
# -----------------------------------------------------------

# /api/v1/products/
class ProductListCreateView(generics.ListCreateAPIView):
    """
    Получение списка товаров и создание нового товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    # Метод create не переопределяем, так как стандартная логика DRF подходит.


# /api/v1/products/<int:pk>/
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление конкретного товара.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# /api/v1/products/reviews/
class ProductReviewsListView(generics.ListAPIView):
    """
    Получение списка товаров с их отзывами и средней оценкой.
    """
    # Добавляем аннотацию для расчета средней оценки
    queryset = Product.objects.annotate(rating=Avg('reviews__stars')) 
    serializer_class = ProductReviewsSerializer


# -----------------------------------------------------------
# REVIEWS
# -----------------------------------------------------------

# /api/v1/reviews/
class ReviewListCreateView(generics.ListCreateAPIView):
    """
    Получение списка отзывов и создание нового отзыва.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    # Метод create не переопределяем, так как стандартная логика DRF подходит.


# /api/v1/reviews/<int:pk>/
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление конкретного отзыва.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer