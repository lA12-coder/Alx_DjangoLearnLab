from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import BookForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created")
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'your_app_label/book_form.html', {'form': form})

@login_required
@permission_required('your_app_label.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, 'your_app_label/book_form.html', {'form': form, 'book': book})
  
  
def book_list(request):
    books = Book.objects.all().order_by('-publication_year', 'title')
    return render(request, 'bookshelf/books_list.html', {'books': books})