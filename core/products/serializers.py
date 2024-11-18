from rest_framework import serializers
from core.products.models import (
    Category,
    Hashtag,
    Keyword,
    Product,
    Service,
    Promotion,
)
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ('id', 'name')


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = (
            'id', 'name', 'description', 'discount_percent',
            'start_date', 'end_date', 'is_active',
            'products', 'services', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError(
                "End date must be after start date"
            )
        return data


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)
    promotions = serializers.SerializerMethodField()
    
    # Fields for receiving IDs during creation/update
    category_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    hashtag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    keyword_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = (
            'id', 'merchant', 'name', 'description', 'price',
            'image', 'categories', 'hashtags', 'keywords',
            'is_active', 'created_at', 'updated_at',
            'category_ids', 'hashtag_ids', 'keyword_ids',
            'promotions'
        )
        read_only_fields = ('id', 'merchant', 'created_at', 'updated_at')

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        hashtag_ids = validated_data.pop('hashtag_ids', [])
        keyword_ids = validated_data.pop('keyword_ids', [])
        
        # Get merchant from current user
        validated_data['merchant'] = self.context['request'].user.merchant
        
        product = Product.objects.create(**validated_data)
        
        # Add relationships
        if category_ids:
            product.categories.set(Category.objects.filter(id__in=category_ids))
        if hashtag_ids:
            product.hashtags.set(Hashtag.objects.filter(id__in=hashtag_ids))
        if keyword_ids:
            product.keywords.set(Keyword.objects.filter(id__in=keyword_ids))
            
        return product

    def get_promotions(self, obj):
        active_promotions = obj.promotions.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        return PromotionSerializer(active_promotions, many=True).data

class ServiceSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    keywords = KeywordSerializer(many=True, read_only=True)
    promotions = serializers.SerializerMethodField()
    
    category_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    hashtag_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    keyword_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Service
        fields = (
            'id', 'merchant', 'name', 'description', 'price',
            'categories', 'hashtags', 'keywords', 'is_active',
            'created_at', 'updated_at',
            'category_ids', 'hashtag_ids', 'keyword_ids',
            'promotions'
        )
        read_only_fields = ('id', 'merchant', 'created_at', 'updated_at')

    def create(self, validated_data):
        category_ids = validated_data.pop('category_ids', [])
        hashtag_ids = validated_data.pop('hashtag_ids', [])
        keyword_ids = validated_data.pop('keyword_ids', [])
        
        validated_data['merchant'] = self.context['request'].user.merchant
        
        service = Service.objects.create(**validated_data)
        
        if category_ids:
            service.categories.set(Category.objects.filter(id__in=category_ids))
        if hashtag_ids:
            service.hashtags.set(Hashtag.objects.filter(id__in=hashtag_ids))
        if keyword_ids:
            service.keywords.set(Keyword.objects.filter(id__in=keyword_ids))
            
        return service

    def get_promotions(self, obj):
        active_promotions = obj.promotions.filter(
            is_active=True,
            start_date__lte=timezone.now(),
            end_date__gte=timezone.now()
        )
        return PromotionSerializer(active_promotions, many=True).data
