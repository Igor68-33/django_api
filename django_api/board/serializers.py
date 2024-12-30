from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import Ad, User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'password']
        read_only_fields = ['id']

    def update(self, instance, validated_data):
        # Обновляем только те поля, которые были переданы
        for attr, value in validated_data.items():
            if value is not None:
                setattr(instance, attr, value)

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            update_session_auth_hash(self.context['request'], instance)

        instance.save()
        return instance


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'price', 'category', 'created_at', 'updated_at', 'user_id']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        return ad
