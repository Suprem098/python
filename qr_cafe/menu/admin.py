from django.contrib import admin
from .models import MenuItem, Order
from unfold.admin import TabularInline , ModelAdmin
from . import models

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'item', 'quantity', 'table_no', 'status')
#     list_display_links = ('id', 'item')
#     list_filter = ('status',)
#     search_fields = ('table_no', 'item__name')

# admin.site.register(MenuItem)
class OrderInline(TabularInline):
    model = models.Order
    extra = 1


@admin.register(models.MenuItem)
class MenuItem(ModelAdmin):
    inlines=[OrderInline]
    
@admin.register(models.Order)
class OrderAdmin(ModelAdmin):
    pass
