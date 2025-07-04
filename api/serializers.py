from rest_framework import serializers
from .models import User, Paragraph


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'dob', 'password', 'createdAt', 'modifiedAt']
        read_only_fields = ['id', 'createdAt', 'modifiedAt']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['id', 'created_at']


class SearchSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=255)
