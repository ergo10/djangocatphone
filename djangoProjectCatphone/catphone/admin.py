from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Catsphone, Supplier, Order, Pos_order, Chegue


class CatsphoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'photo_show', 'supplier', 'exist')  # Отображение полей
    list_display_links = ('id', 'name')  # Установка ссылок на атрибуты
    search_fields = ('name', 'price')  # Поиск по полям
    list_editable = ('price', 'exist')  # Изменяемое поле
    list_filter = ('exist', 'supplier')

    def photo_show(self, obj):
        if obj.photo:
            return mark_safe("<img src='{}' width='60' />".format(obj.photo.url))
        return "None"

    photo_show.__name__ = "Картинка"


admin.site.register(Catsphone, CatsphoneAdmin)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'agent_firstname', 'agent_name', 'agent_patronymic', 'exist')  # Отображение полей
    list_display_links = ('id', 'title')  # Установка ссылок на атрибуты
    search_fields = ('title', 'agent_firstname')  # Поиск по полям
    list_editable = ('exist',)  # Изменяемое поле
    list_filter = ('exist',)  # Фильтры полей


admin.site.register(Supplier, SupplierAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'date_finish', 'status', 'price', 'address_delivery')  # Отображение полей
    list_display_links = ('id',)  # Установка ссылок на атрибуты
    search_fields = ('date_create', 'address_delivery')  # Поиск по полям
    list_editable = ('date_finish', 'status')  # Изменяемое поле
    list_filter = ('status',)  # Фильтры полей


admin.site.register(Order, OrderAdmin)


class Pos_orderAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'order', 'count_product', 'price')  # Отображение полей
    list_display_links = ('product', 'order')  # Установка ссылок на атрибуты
    search_fields = ('product', 'order')  # Поиск по полям


admin.site.register(Pos_order, Pos_orderAdmin)


# Cheque
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('order', 'date_print', 'address_print', 'terminal')  # Отображение полей
    list_display_links = ('order', 'date_print')  # Установка ссылок на атрибуты
    search_fields = ('date_print', 'address_print')  # Поиск по полям


admin.site.register(Chegue, ChequeAdmin)
