from django import forms
from .models import Book  # or any model you want the form to use

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']  # replace with your model fields
