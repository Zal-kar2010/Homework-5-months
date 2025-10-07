"""
URL configuration for shop_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Categories
    # 1. ОБНОВЛЕННЫЙ ПУТЬ: /api/v1/categories/ теперь использует View с подсчетом товаров
    path(
        'api/v1/categories/', 
        views.CategoryProductCountListView.as_view(), 
        name='category-list-with-count'
    ),
    path(
        'api/v1/categories/<int:pk>/', 
        views.CategoryDetailView.as_view(), 
        name='category-detail'
    ),

    # Products
    # 2. НОВЫЙ ПУТЬ: /api/v1/products/reviews/ для вывода продуктов с рейтингом
    path(
        'api/v1/products/reviews/', 
        views.ProductReviewsListView.as_view(), 
        name='product-list-with-reviews'
    ),
    # Старый путь для стандартного списка продуктов остается
    path(
        'api/v1/products/', 
        views.ProductListView.as_view(), 
        name='product-list'
    ),
    path(
        'api/v1/products/<int:pk>/', 
        views.ProductDetailView.as_view(), 
        name='product-detail'
    ),

    # Reviews
    path('api/v1/reviews/', views.ReviewListView.as_view(), name='review-list'),
    path('api/v1/reviews/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
]
