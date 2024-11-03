from django.contrib import admin
from .models import (
    ScrapedCategory,
    ScrapedItem,
    ScrapedItemImage,  # Include ScrapedItemImage
    ScrapedOrderItem,
    ScrapedOrder,
    ScrapedBillingAddress,
    ScrapedPayment,
    ScrapedCoupon,
    ScrapedRefund
)

class ScrapedItemImageInline(admin.TabularInline):
    model = ScrapedItemImage
    extra = 1  # Provides one empty slot for adding new images
    readonly_fields = ['image']  # Makes images readonly
    fields = ['image']  # Displays only the image field

@admin.register(ScrapedItem)
class ScrapedItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'discount_price', 'category', 'label', 'slug', 'is_active')
    list_filter = ('category', 'label', 'is_active')
    search_fields = ('title', 'description_short', 'description_long')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ScrapedItemImageInline]  # Add ScrapedItemImage as inline

@admin.register(ScrapedCategory)
class ScrapedCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ScrapedOrderItem)
class ScrapedOrderItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity', 'ordered', 'get_total_item_price')
    list_filter = ('ordered',)
    search_fields = ('user__username', 'item__title')

@admin.register(ScrapedOrder)
class ScrapedOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'ref_code', 'start_date', 'ordered_date', 'ordered', 'get_total')
    list_filter = ('ordered', 'being_delivered', 'received')
    search_fields = ('user__username', 'ref_code')
    readonly_fields = ('get_total',)

@admin.register(ScrapedBillingAddress)
class ScrapedBillingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'street_address', 'apartment_address', 'country', 'zip', 'address_type', 'default')
    search_fields = ('user__username', 'street_address', 'apartment_address')

@admin.register(ScrapedPayment)
class ScrapedPaymentAdmin(admin.ModelAdmin):
    list_display = ('stripe_charge_id', 'user', 'amount', 'timestamp')
    search_fields = ('stripe_charge_id', 'user__username')

@admin.register(ScrapedCoupon)
class ScrapedCouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount')
    search_fields = ('code',)

@admin.register(ScrapedRefund)
class ScrapedRefundAdmin(admin.ModelAdmin):
    list_display = ('order', 'reason', 'accepted', 'email')
    search_fields = ('order__ref_code', 'email')
