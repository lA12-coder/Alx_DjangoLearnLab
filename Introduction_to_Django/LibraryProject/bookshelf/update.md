from bookshelf.models import Book

book = Book.objects.all()
book.save()
print(book.title) 

Nineteen Eighty-Four
