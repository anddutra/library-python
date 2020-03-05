from rest_framework.test import APIClient, APITestCase
from book.models import Book, Author, AuthorBook

class TestBook(APITestCase):
    """
    Tests of Book
    """

    def setUp(self):
        """
        Setting up books' test.
        """
        self.url = '/bookapi/'
        self.author1 = self.setup_author('J. K. Rowling')
        self.book1 = self.setup_book("Harry Potter and the Philosopher’s Stone", self.author1, 1, 1997)
        self.author2 = self.setup_author('J. R. R. Tolkien')
        self.book2 = self.setup_book("The Lord of the Rings: The Fellowship of the Ring", self.author2, 1, 1954)
        self.author3 = self.setup_author('George R. R. Martin')
        self.client = APIClient()

    @staticmethod
    def setup_author(name):
        """
        Create authors to test.
        """
        return Author.objects.create(name=name)

    @staticmethod
    def setup_book(name, author, edition, year):
        """
        Create books to test.
        """
        book =  Book.objects.create(name=name, edition=edition, publication_year=year)
        AuthorBook.objects.create(book=book, author=author)
        return book

    def test_get_books(self):
        """
        Test get all books.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 2)

    def test_get_book_page2(self):
        """
        Test get page 2 of all books.
        """
        response = self.client.get(self.url+str('?page=2'), format='json')
        self.assertEqual(response.status_code, 404)

    def test_get_book_by_name(self):
        """
        Test get book by name.
        """
        response = self.client.get(self.url+str('?search=Harry Potter'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 1)

    def test_get_book_by_year(self):
        """
        Test get book by year.
        """
        response = self.client.get(self.url+str('?search=1997'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 1)

    def test_get_book_by_edition(self):
        """
        Test get book by edition.
        """
        response = self.client.get(self.url+str('?search=1'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 2)

    def test_get_book_by_author(self):
        """
        Test get book by author.
        """
        response = self.client.get(self.url+str('?search=J. R. R. Tolkien'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 1)

    def test_create_book(self):
        """
        Test create book
        """
        json = (
            "{"
            '"authorsbook": [{"author":' + str(self.author3.id) + '}],'
            '"name": "A Song of Ice and Fire: A Game of Thrones",'
            '"edition": 1,'
            '"publication_year": 1996'
            "}"
        )
        response = self.client.post(self.url, data=json, content_type="application/json")
        self.assertEqual(response.status_code, 201)
        
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 3)

    def test_update_book(self):
        """
        Test update book
        """
        json = (
            "{"
            '"authorsbook": [{"author":' + str(self.author1.id) + '}],'
            '"name": "Harry Potter and the Philosopher’s Stone - Update",'
            '"edition": 1,'
            '"publication_year": 1997'
            "}"
        )
        response = self.client.put(self.url+str(self.book1.id)+'/', data=json, content_type="application/json")
        self.assertEqual(response.status_code, 200)
        
        response = self.client.get(self.url+str('?search=Update'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 1)
    
    def test_delete_book(self):
        """
        Test delete book
        """
        response = self.client.delete(self.url+str(self.book1.id)+'/', format='json')
        self.assertEqual(response.status_code, 204)