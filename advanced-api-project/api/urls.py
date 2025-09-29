from django.urls import path, include
from .views import  *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'author', AuthorViewSet)

urlpatterns  = [
    path("books/", BookListView.as_view() , name = 'book_list'),
    path("books/<int:pk>/", BookDetailView.as_view() , name = 'book-detail'),
    path("books/create/", BookCreateView.as_view() , name = 'book_create'),
    path("books/delete/<int:pk>/", BookDeleteView.as_view() , name = 'book_delete'),
    path("books/update/<int:pk>/", BookUpdateView.as_view() , name = 'book_update'),
    path('', include(router.urls)),
]