# views.py
from rest_framework import generics
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
# Categories: Добавляем создание, изменение и удаление
# -----------------------------------------------------------

# Эндпоинт: /api/v1/categories/
# Обеспечивает: GET (список с products_count) и POST (создание)
class CategoryListCreateView(generics.ListCreateAPIView):
    # Для GET-запроса (списка) используем сериализатор с products_count
    def get_queryset(self):
        # Используем аннотирование (Count) для подсчета товаров в каждой категории
        return Category.objects.annotate(products_count=Count('products'))
    
    def get_serializer_class(self):
        # Для LIST (GET) используем сериализатор с количеством товаров
        if self.request.method == 'GET':
            return CategoryProductCountSerializer
        # Для CREATE (POST) используем базовый сериализатор для записи
        return CategorySerializer


# Эндпоинт: /api/v1/categories/<int:pk>/
# Обеспечивает: GET (один), PUT/PATCH (изменение), DELETE (удаление)
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # lookup_field по умолчанию 'pk', но можно использовать 'id'
    # Если в URL /<int:id>/, то нужно было бы установить: lookup_field = 'id'


# -----------------------------------------------------------
# Products: Добавляем создание, изменение и удаление
# -----------------------------------------------------------

# Эндпоинт: /api/v1/products/
# Обеспечивает: GET (список) и POST (создание)
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Эндпоинт: /api/v1/products/<int:pk>/
# Обеспечивает: GET (один), PUT/PATCH (изменение), DELETE (удаление)
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# Отдельный эндпоинт для списка товаров с отзывами и рейтингом
# Эндпоинт: /api/v1/products/reviews/ (или /api/v1/product-reviews/)
class ProductReviewsListView(generics.ListAPIView):
    # Используем аннотирование (Avg) для вычисления среднего балла (stars)
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductReviewsSerializer


# -----------------------------------------------------------
# Reviews: Добавляем создание, изменение и удаление
# -----------------------------------------------------------

# Эндпоинт: /api/v1/reviews/
# Обеспечивает: GET (список) и POST (создание)
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


# Эндпоинт: /api/v1/reviews/<int:pk>/
# Обеспечивает: GET (один), PUT/PATCH (изменение), DELETE (удаление)
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

# Удалены старые классы (CategoryDetailView, ProductDetailView, ReviewListView, ReviewDetailView),
# так как их функционал теперь включен в новые классы.