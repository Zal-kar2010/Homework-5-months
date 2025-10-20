from rest_framework import serializers
from .models import User, random

# Сериализатор регистрации
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.confirmation_code = str(random.randint(100000, 999999))
        user.is_active = False  # пока не подтвержден
        user.save()
        return user


# Сериализатор подтверждения
class ConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(username=attrs['username'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден.")

        if user.confirmation_code != attrs['code']:
            raise serializers.ValidationError("Неверный код подтверждения.")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        user.is_active = True
        user.confirmation_code = ''  # код больше не нужен
        user.save()
        return user
