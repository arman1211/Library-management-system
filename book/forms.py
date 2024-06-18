from django import forms
from . import models

class BookForm(forms.ModelForm):
    class Meta:
        model = models.BookModel
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.ReviewModel
        fields = ['rating','review']