from django.test import TestCase

# Create your tests here.
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Book, Author

class BookCreateTests(APITestCase):

    def setUp(self):
        # Create an author and a user for authentication
        self.author = Author.objects.create(name="Test Author")
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = '/api/books/'
        self.client.login(username='testuser', password='testpassword')

    def test_create_book(self):
        # Test that a book can be created
        data = {
            'title': 'Test Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'Test Book')

    def test_create_book_without_authentication(self):
        # Test that a book cannot be created without authentication
        self.client.logout()
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2024,
            'author': self.author.id
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #Next, test that you can retrieve a single book by its ID.
class BookDetailTests(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2024, author=self.author
        )
        self.url = f'/api/books/{self.book.id}/'

    def test_get_book_detail(self):
        # Test retrieving book details by ID
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2024)

        #Now, let’s test the update functionality.
class BookUpdateTests(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2024, author=self.author
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = f'/api/books/{self.book.id}/'

    def test_update_book(self):
        # Test that a book can be updated
        data = {
            'title': 'Updated Test Book',
            'publication_year': 2025,
            'author': self.author.id
        }
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Test Book')
        self.assertEqual(self.book.publication_year, 2025)

    def test_update_book_unauthorized(self):
        # Test that only an authenticated user can update a book
        self.client.logout()
        data = {'title': 'Unauthorized Update'}
        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


       #Testing the deletion of a book:
class BookDeleteTests(APITestCase):

    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book", publication_year=2024, author=self.author
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.url = f'/api/books/{self.book.id}/'

    def test_delete_book(self):
        # Test that a book can be deleted
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_book_unauthorized(self):
        # Test that a book cannot be deleted by an unauthorized user
        self.client.logout()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

       #Test the filtering, searching, and ordering features on the BookListView:
class BookListTests(APITestCase):

    def setUp(self):
        self.author1 = Author.objects.create(name="Author One")
        self.author2 = Author.objects.create(name="Author Two")
        Book.objects.create(title="Book A", publication_year=2020, author=self.author1)
        Book.objects.create(title="Book B", publication_year=2021, author=self.author2)
        Book.objects.create(title="Book C", publication_year=2022, author=self.author1)
        self.url = '/api/books/'

    def test_filter_by_author(self):
        response = self.client.get(self.url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_by_title(self):
        response = self.client.get(self.url, {'search': 'Book A'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_by_publication_year(self):
        response = self.client.get(self.url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'Book A')

        
