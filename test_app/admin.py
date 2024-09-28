from django.contrib import admin
from .models import Category ,WordPair
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

admin.site.register(Category, CategoryAdmin)

class WordPairAdmin(admin.ModelAdmin):
    list_display = ('id', 'word_ko', 'word_uz', 'category')

admin.site.register(WordPair, WordPairAdmin)