from bookshelf.models import Book

book = Book.objects.all()
book.delete()
# (1, {'bookshelf.Book': 1})