from django.contrib import admin
from core.products.models import (
    Category,
    Hashtag,
    Keyword,
    Product,
    Service,
    Promotion,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at', 'updated_at')


class PromotionInline(admin.TabularInline):
    model = Promotion.products.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'categories')
    search_fields = ('name', 'description', 'merchant__name')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('categories', 'hashtags', 'keywords')
    inlines = [PromotionInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('merchant')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'merchant', 'price', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'categories')
    search_fields = ('name', 'description', 'merchant__name')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('categories', 'hashtags', 'keywords')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('merchant')


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('products', 'services')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'discount_percent')
        }),
        ('Timing', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Products & Services', {
            'fields': ('products', 'services')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
