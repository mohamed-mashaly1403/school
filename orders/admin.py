from django.contrib import admin

# Register your models here.
from .models import Payment,Order,orderPoduct,orderPoductClasses
class orderPoductInline(admin.TabularInline):
    model = orderPoduct
    extra = 0
    readonly_fields = [field.name for field in orderPoduct._meta.fields]

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','total','is_ordered','created_at']
    list_filter = ['status','is_ordered']
    list_editable = ['is_ordered']
    list_per_page = 10
    inlines = [orderPoductInline]

admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(orderPoduct)
admin.site.register(orderPoductClasses)