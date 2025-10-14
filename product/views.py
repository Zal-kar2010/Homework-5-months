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
    def get_queryset(self):
        # Подсчёт количества товаров в каждой категории
        return Category.objects.annotate(products_count=Count('products'))

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryProductCountSerializer
        return CategorySerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # вызывает validate_* из сериализатора
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# /api/v1/categories/<int:pk>/
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# -----------------------------------------------------------
# PRODUCTS
# -----------------------------------------------------------

# /api/v1/products/
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Проверка всех правил из serializers.py
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# /api/v1/products/<int:pk>/
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# /api/v1/products/reviews/
class ProductReviewsListView(generics.ListAPIView):
    queryset = Product.objects.annotate(rating=Avg('reviews__stars'))
    serializer_class = ProductReviewsSerializer


# -----------------------------------------------------------
# REVIEWS
# -----------------------------------------------------------

# /api/v1/reviews/
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Проверка: text, stars, product_id
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# /api/v1/reviews/<int:pk>/
class ReviewRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
