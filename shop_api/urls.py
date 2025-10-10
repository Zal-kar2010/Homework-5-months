# shop_api/urls.py (ИСПРАВЛЕННЫЙ)
from django.contrib import admin
from django.urls import path
from product import views # Ваш импорт views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Categories
    # 1. Списковый/Создание: GET (с count) и POST
    path(
        'api/v1/categories/', 
        # ИСПРАВЛЕНИЕ: Заменяем CategoryProductCountListView на CategoryListCreateView
        views.CategoryListCreateView.as_view(), 
        name='category-list-create'
    ),
    # 2. Детальный/Изменение/Удаление: GET, PUT, PATCH, DELETE
    path(
        'api/v1/categories/<int:pk>/', 
        # ИСПРАВЛЕНИЕ: Заменяем CategoryDetailView на CategoryRetrieveUpdateDestroyView
        views.CategoryRetrieveUpdateDestroyView.as_view(), 
        name='category-retrieve-update-destroy'
    ),

    # Products
    # 3. Товары с отзывами и рейтингом (Только GET)
    path(
        'api/v1/products/reviews/', 
        views.ProductReviewsListView.as_view(), 
        name='product-list-with-reviews'
    ),
    # 4. Списковый/Создание: GET list, POST create
    path(
        'api/v1/products/', 
        # ИСПРАВЛЕНИЕ: Заменяем ProductListView на ProductListCreateView
        views.ProductListCreateView.as_view(), 
        name='product-list-create'
    ),
    # 5. Детальный/Изменение/Удаление: GET, PUT, PATCH, DELETE
    path(
        'api/v1/products/<int:pk>/', 
        # ИСПРАВЛЕНИЕ: Заменяем ProductDetailView на ProductRetrieveUpdateDestroyView
        views.ProductRetrieveUpdateDestroyView.as_view(), 
        name='product-retrieve-update-destroy'
    ),

    # Reviews
    # 6. Списковый/Создание: GET list, POST create
    path(
        'api/v1/reviews/', 
        # ИСПРАВЛЕНИЕ: Заменяем ReviewListView на ReviewListCreateView
        views.ReviewListCreateView.as_view(), 
        name='review-list-create'
    ),
    # 7. Детальный/Изменение/Удаление: GET, PUT, PATCH, DELETE
    path(
        'api/v1/reviews/<int:pk>/', 
        # ИСПРАВЛЕНИЕ: Заменяем ReviewDetailView на ReviewRetrieveUpdateDestroyView
        views.ReviewRetrieveUpdateDestroyView.as_view(), 
        name='review-retrieve-update-destroy'
    ),
]