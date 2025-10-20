# shop_api/urls.py (КОРРЕКТНЫЙ ФАЙЛ)

from django.contrib import admin
from django.urls import path, include

# Импорт из вашего приложения product
from product import views 

# --- ИМПОРТ ДЛЯ АВТОРИЗАЦИИ И РЕГИСТРАЦИИ (ДОБАВИТЬ ЭТО) ---
# Предполагаем, что ваши View's находятся в приложении 'users'
from users.views import RegistrationView, ConfirmationView, LoginView
from rest_framework_simplejwt.views import TokenRefreshView 
# -----------------------------------------------------------

urlpatterns = [
    path('admin/', admin.site.urls),

    # Categories
    # 1. Списковый/Создание: GET (с count) и POST
    path(
        'api/v1/categories/', 
        views.CategoryListCreateView.as_view(), 
        name='category-list-create'
    ),
    # 2. Детальный/Изменение/Удаление: GET, PUT, PATCH, DELETE
    path(
        'api/v1/categories/<int:pk>/', 
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
        views.ProductListCreateView.as_view(), 
        name='product-list-create'
    ),
    # 5. Детальный/Изменение/Удаление: GET, PUT, PATCH, DELETE
    path(
        'api/v1/products/<int:pk>/', 
        views.ProductRetrieveUpdateDestroyView.as_view(), 
        name='product-retrieve-update-destroy'
    ),

    # Reviews
    # 6. Списковый/Создание: GET list, POST create
    path(
        'api/v1/reviews/', 
        views.ReviewListCreateView.as_view(), 
        name='review-list-create'
    ),
    # 7. Детальный/Изменение/Удаление: GET, PUT, PATCH, DELETE
    path(
        'api/v1/reviews/<int:pk>/', 
        views.ReviewRetrieveUpdateDestroyView.as_view(), 
        name='review-retrieve-update-destroy'
    ),

    # --- ПУТИ АВТОРИЗАЦИИ И РЕГИСТРАЦИИ ---
    # 1. Регистрация
    path('api/v1/users/register/', RegistrationView.as_view(), name='register'),
    
    # 2. Подтверждение пользователя
    path('api/v1/users/confirm/', ConfirmationView.as_view(), name='confirm_user'),
    
    # 3. Авторизация (Login) - Получение access/refresh токенов
    path('api/v1/users/login/', LoginView.as_view(), name='token_obtain_pair'),
    
    # 4. Обновление токена
    path('api/v1/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # ---------------------------------------

]