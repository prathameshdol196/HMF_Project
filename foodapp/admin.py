from django.contrib import admin
from .models import User, FoodMakerProfile, EaterProfile, FoodItem

admin.site.register(User)
admin.site.register(FoodMakerProfile)
admin.site.register(EaterProfile)
admin.site.register(FoodItem)


from .models import PromoCode

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount", "valid_from", "valid_to", "is_active")
    search_fields = ("code",)
    list_filter = ("is_active", "valid_from", "valid_to")

