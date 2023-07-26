from rest_framework import serializers

from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'password', 'password2', 'name', 'phone', 'city', 'avatar']

    def save(self, *args, **kwargs):
        """Метод для сохранения нового пользователя"""
        # Создаём объект класса User
        name = self.validated_data['name'] if 'name' in self.validated_data else None
        phone = self.validated_data['phone'] if 'phone' in self.validated_data else None
        city = self.validated_data['city'] if 'city' in self.validated_data else None
        avatar = self.validated_data['avatar'] if 'avatar' in self.validated_data else None

        user = User.objects.create(
            email=self.validated_data['email'],
            name=name,
            phone=phone,
            city=city,
            avatar=avatar,
        )
        # Проверяем на валидность пароли
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)

        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'phone', 'city', 'avatar')