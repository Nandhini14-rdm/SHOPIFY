from django.contrib import admin
from .models import Category
from .models import Products

"""
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description')

"""
admin.site.register(Category)
admin.site.register(Products)