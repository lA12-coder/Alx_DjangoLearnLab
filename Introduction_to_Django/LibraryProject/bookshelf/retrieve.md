from bookshelf.models import Book

books = Book.objects.all()
for book in books:
    print(f"Title:{book.title}, Author:{book.author}, Publication_year:{book.publication_year}")

# Title:1984, Author:George Orwell, Publication_year:1949