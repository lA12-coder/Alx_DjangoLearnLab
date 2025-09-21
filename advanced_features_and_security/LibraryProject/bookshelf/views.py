from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import ExampleForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from django.db.models import Q

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created")
            return redirect('book_list')
    else:
        form = ExampleForm()
    return render(request, 'your_app_label/book_form.html', {'form': form})

@login_required
@permission_required('your_app_label.can_edit', raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated.")
            return redirect('book_detail', pk=book.pk)
    else:
        form = ExampleForm(instance=book)
    return render(request, 'your_app_label/book_form.html', {'form': form, 'book': book})
  
  
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def books_list(request):
    """
    Safe search: use Q objects & ORM to prevent injection.
    Avoid building SQL strings with user input.
    """
    query = request.GET.get('q', '').strip()
    books = Book.objects.all()
    if query:
        # Parameterized via ORM, safe from SQL injection
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )
    # paginate if needed
    return render(request, 'bookshelf/book_list.html', {'books': books})
