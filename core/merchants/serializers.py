from rest_framework import serializers
from core.merchants.models import Merchant
from core.accounts.serializers import UserSerializer


class MerchantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Merchant
        fields = ('id', 'user', 'name', 'description', 'logo', 'address', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context['request'].user
        if Merchant.objects.filter(user=user).exists():
            raise serializers.ValidationError("User already has a merchant account")
        return Merchant.objects.create(user=user, **validated_data)
