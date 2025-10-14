from rest_framework import serializers
from .models import Category, Product, Review
from django.db.models import Count, Avg


# --- CATEGORY SERIALIZER ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    # Валидация имени категории
    def validate_name(self, value):
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Название категории должно содержать не менее 2 символов.")
        if Category.objects.filter(name__iexact=value).exclude(id=self.instance.id if self.instance else None).exists():
            raise serializers.ValidationError("Категория с таким названием уже существует.")
        return value

    # Общая проверка
    def validate(self, attrs):
        if not attrs.get("name"):
            raise serializers.ValidationError({"name": "Название категории обязательно."})
        return attrs


# --- PRODUCT SERIALIZER ---
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'category_id']

    # Валидация названия
    def validate_title(self, value):
        if not value or len(value.strip()) < 2:
            raise serializers.ValidationError("Название продукта должно быть не короче 2 символов.")
        return value.strip()

    # Валидация цены
    def validate_price(self, value):
        if value is None:
            raise serializers.ValidationError("Цена обязательна.")
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value

    # Общая валидация
    def validate(self, attrs):
        category = attrs.get('category')
        title = attrs.get('title')
        # Проверка на уникальность продукта в категории
        if category and title:
            exists = Product.objects.filter(title__iexact=title, category=category)
            if self.instance:
                exists = exists.exclude(id=self.instance.id)
            if exists.exists():
                raise serializers.ValidationError(
                    f"Продукт с названием '{title}' уже существует в этой категории."
                )
        return attrs


# --- REVIEW SERIALIZER ---
class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    stars = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product', 'product_id']

    # Проверка текста отзыва
    def validate_text(self, value):
        if not value or len(value.strip()) < 5:
            raise serializers.ValidationError("Текст отзыва должен содержать минимум 5 символов.")
        return value.strip()

    # Проверка звёзд
    def validate_stars(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Оценка должна быть от 1 до 5.")
        return value

    # Общая проверка
    def validate(self, attrs):
        product = attrs.get("product")
        text = attrs.get("text")

        if product is None:
            raise serializers.ValidationError({"product_id": "Поле product_id обязательно."})

        if Review.objects.filter(product=product, text=text).exclude(
            id=self.instance.id if self.instance else None
        ).exists():
            raise serializers.ValidationError("Такой отзыв для этого продукта уже существует.")

        return attrs


# --- ДОПОЛНИТЕЛЬНЫЕ СЕРИАЛИЗАТОРЫ ДЛЯ GET-ЭНДПОИНТОВ ---
class NestedReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars']


class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = NestedReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'rating', 'reviews']

    def get_rating(self, product):
        avg = product.reviews.aggregate(avg=Avg('stars'))['avg']
        return round(avg, 2) if avg else 0.0


class CategoryProductCountSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, category):
        return getattr(category, 'products_count', 0)