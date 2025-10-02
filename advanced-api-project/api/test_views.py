from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .factories import BookFactory
from .serializers import BookSerializer


class BookAPITests(APITestCase):
    def setUp(self):
        """Create a user and log in for all tests."""
        User = get_user_model()
        self.username = "u"
        self.password = "p"
        self.user = User.objects.create_user(
            username=self.username, password=self.password
        )
        # Perform a real login with credentials
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)  # sanity check: make sure login worked

    def test_create_book(self):
        url = reverse("book_create")
        book = BookFactory.create()
        serialized_book = BookSerializer(book).data

        response = self.client.post(url, serialized_book, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], book.title)
        self.assertEqual(response.data["author"], book.author.id)

    def test_update_book(self):
        book = BookFactory.create()
        # If you have a named URL, prefer reverse("book_update", args=[book.id])
        url = f"/api/books/update/{book.id}/"

        response = self.client.patch(url, {"title": "updated"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "updated")

    def test_delete_book(self):
        book = BookFactory.create()
        # If you have a named URL, prefer reverse("book_delete", args=[book.id])
        url = f"/api/books/delete/{book.id}/"

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
