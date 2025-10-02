from django.utils import timezone
from rest_framework import serializers
from .models import Author
from .models import Book

# The BookSerializer is nested on the AuthorSerializer
class BookSerializer(serializers.ModelSerializer):


    class Meta:
        model = Book
        fields= '__all__'

    def validate_publication_year(self, value):
        current_year = timezone.now().year
        if value > current_year:
            raise  serializers.ValidationError("Publication year can not be in the future!")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'book']

