from rest_framework import generics
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Ad, User
from .serializers import UserSerializer, UserRegistrationSerializer, AdSerializer


# 7 Авторизация открыт POST	http://127.0.0.1:8000/api/token/login/
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


# 3 защищенный канал посмотреть себя
class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# 5 Изменить свою закрыт PUT	http://127.0.0.1:8000/api/user/update/
class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# 6 удаление своей записи
class UserDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        # Удаляем токен (если используется токен аутентификации)
        Token.objects.filter(user=user).delete()
        self.perform_destroy(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 1 список всех пользователей для всех
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#  4 карточка пользователя
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 3 создать своё объявление
class AdCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Устанавливаем текущего пользователя как автора объявления


# 1 Список объявлений для всех
class AdsListView(generics.ListAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


#  2 объявление по ид
class AdDetailView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = 'id'  # Используем 'id' как поле для поиска


# 4 обновление своего объявления
class AdUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    lookup_field = 'id'

    def perform_update(self, serializer):
        ad = self.get_object()
        if ad.user.id != self.request.user.id:
            raise PermissionDenied('У вас нет прав для изменения этого объявления.')
        serializer.save()


# 5 удаление своего объявления
class AdDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def perform_destroy(self, instance):
        if instance.user.id != self.request.user.id:
            raise PermissionDenied('У вас нет прав для удаления этого объявления.')
        instance.delete()


# 2 список объявлений пользователя по ид
class UserAdsList(generics.ListAPIView):
    serializer_class = AdSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Ad.objects.filter(user=user_id)
