import factory
from .models import Author, Book

class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author
        
    name = factory.Faker('name')
    
class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book
        
    title = factory.Faker('sentence', nb_words=3)
    publication_year = factory.Faker('year')
    author = factory.SubFactory(AuthorFactory)