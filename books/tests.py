from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Book, Review

# Create your tests here.
class BookTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = 'reviewuser',
            email = 'reviewuser@mail.com',
            password = 'testpass123'
        )

        self.book = Book.objects.create(
            title = 'Harry Poter',
            author = 'jk howling',
            price = '25.00'
        )

        self.review = Review.objects.create(
            book = self.book,
            review = "Its a awesome book.",
            author = self.user
        )

    def test_book_listing(self):
        self.assertEqual(f'{self.book.title}', 'Harry Poter')
        self.assertEqual(f'{self.book.author}', 'jk howling')
        self.assertEqual(f'{self.book.price}', '25.00')

    def test_book_list_view(self):
        response = self.client.get(reverse('book_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Harry Poter')
        self.assertTemplateUsed(response, 'books/book_list.html')

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get('/books/12345/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Harry Poter')
        self.assertContains(response, "Its a awesome book.")
        self.assertTemplateUsed(response, 'books/book_detail.html')


