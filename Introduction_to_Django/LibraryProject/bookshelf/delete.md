from bookshelf.models import Book

books = Book.objects.all()
books.delete()
# (1, {'bookshelf.Book': 1})