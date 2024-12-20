from rest_framework import serializers
from django.contrib.auth import get_user_model
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = PhoneNumberField(required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone')
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', '')
        )
        return user

    def validate_phone(self, value):
        if value and not value.is_valid():
            raise serializers.ValidationError(
                "Invalid phone number format. Please use format: +84xxxxxxxxx"
            )
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
