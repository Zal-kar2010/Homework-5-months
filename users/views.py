from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView # Оставляем для LoginView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistrationSerializer, ConfirmSerializer


## -----------------------------------------------------------
## АУТЕНТИФИКАЦИЯ И РЕГИСТРАЦИЯ
## -----------------------------------------------------------

class RegistrationView(generics.CreateAPIView):
    """
    Регистрация нового пользователя.
    """
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        code = user.confirmation_code
        
        # Стандартный ответ 201 CREATED
        return Response({
            "message": "Пользователь создан. Введите код подтверждения.",
            "code": code  # Временно для теста. В продакшене лучше не возвращать.
        }, status=status.HTTP_201_CREATED)


class ConfirmationView(generics.CreateAPIView):
    """
    Подтверждение аккаунта с помощью кода.
    Используем CreateAPIView, так как это POST-запрос, 
    хотя он и не создает новую модель.
    """
    serializer_class = ConfirmSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Вызываем save(), который выполняет логику подтверждения в сериализаторе
        serializer.save()
        
        # Возвращаем 200 OK, так как подтверждение является успешным действием.
        return Response({"message": "Пользователь успешно подтвержден!"}, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
    Вход пользователя и генерация JWT-токенов. 
    Используем APIView для нестандартной логики аутентификации.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not user.is_active:
            return Response({'error': 'Аккаунт не активирован!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Генерация токенов
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': f'Добро пожаловать, {user.username}!'
        })