from bookshelf.models import Book

<!-- Create a Book instance -->

new_book = Book(title='1984',author="George Orwell",publication_year=1949)
new_book.save()


# Retrieve a book instance
from bookshelf.models import Book

books = Book.objects.all()
for book in books:
    print(f"Title:{book.title}, Author:{book.author}, Publication_year:{book.publication_year}")

# Title:1984, Author:George Orwell, Publication_year:1949

# update a book instance
from bookshelf.models import Book

book = Book.objects.all()
book.save()
print(book.title)
# Nineteen Eight-Four


# Delete the book instance
from bookshelf.models import Book

books = Book.objects.all()
books.delete()
# (1, {'bookshelf.Book': 1})