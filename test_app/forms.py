from django import forms
from .models import WordPair, Category

class WordPairForm(forms.ModelForm):
    class Meta:
        model = WordPair
        fields = ['word_ko', 'word_uz', 'category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields  = ['name']
