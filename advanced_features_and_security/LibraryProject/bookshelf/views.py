from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import ExampleForm  # <-- add this import

# Existing permission-based views
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # Use ExampleForm to create a book
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Book created successfully.")
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Editing book: {book.title}")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return HttpResponse(f"Deleted book: {book.title}")

#edited
