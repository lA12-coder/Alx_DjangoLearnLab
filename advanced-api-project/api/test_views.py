import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from .factories import BookFactory, AuthorFactory
from rest_framework.test import APIClient
from .serializers import BookSerializer


@pytest.mark.django_db
def test_create_book():
    client = APIClient()

    #create and authenticate the user
    User = get_user_model()
    user = User.objects.create_user(username='u', password='p')
    client.force_authenticate(user=user)

    url = reverse('book_create')
    book = BookFactory.create()
    serialized_book = BookSerializer(book).data
    resp = client.post(url,serialized_book, format='json' )
    assert resp.status_code == 201
    assert resp.data['title'] == book.title
    assert resp.data['author'] == book.author.id

@pytest.mark.django_db
def test_update_book():
    client = APIClient()
    #create and authenticate the user
    User = get_user_model()
    user = User.objects.create_user(username='u', password='p')
    client.force_authenticate(user=user)

    book = BookFactory.create()
    url= '/api/books/update/' + f'{book.id}/'
    resp = client.patch(url,{'title': 'updated'}, format='json' )
    assert resp.status_code == 200
    assert resp.data['title'] == 'updated'

@pytest.mark.django_db
def test_delete_book():
    client = APIClient()
    #create and authenticate the user
    User = get_user_model()
    user = User.objects.create_user(username='u', password='p')
    client.force_authenticate(user=user)

    book = BookFactory.create()
    url= '/api/books/delete/' + f'{book.id}/'
    resp = client.delete(url)
    assert resp.status_code == status.HTTP_204_NO_CONTENT
