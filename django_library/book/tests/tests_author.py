from rest_framework.test import APIClient, APITestCase
from book.models import Author

class TestAuthor(APITestCase):
    """
    Tests of Author
    """

    def setUp(self):
        """
        Setting up authors' test.
        """
        self.url = '/authorapi/'
        self.author1 = self.setup_author('Stephen King')
        self.author2 = self.setup_author('J. K. Rowling')
        self.author3 = self.setup_author('Neil Gaiman')
        self.author4 = self.setup_author('J. R. R. Tolkien')
        self.author5 = self.setup_author('George R. R. Martin')
        self.client = APIClient()

    @staticmethod
    def setup_author(name):
        """
        Create authors to test.
        """
        return Author.objects.create(name=name)

    def test_get_authors(self):
        """
        Test get all authors.
        """
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 5)

    def test_get_authors_page2(self):
        """
        Test get page 2 of all authors.
        """
        response = self.client.get(self.url+str('?page=2'), format='json')
        self.assertEqual(response.status_code, 404)

    def test_get_authors_by_name(self):
        """
        Test get author by name.
        """
        response = self.client.get(self.url+str('?search=Stephen'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 1)

    def test_get_authors_by_name_return_empty(self):
        """
        Test get author by an inexistent name.
        """
        response = self.client.get(self.url+str('?search=Andre'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 0)

    def test_get_authors_by_name_return_two(self):
        """
        Test get authors by a common name.
        """
        response = self.client.get(self.url+str('?search=R. R.'), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.data["count"], 2)

    def test_create_author(self):
        """
        Test create author
        """
        json = (
            "{"
            '"name": "Alan Moore"'
            "}"
        )
        response = self.client.post(self.url, data=json, content_type="application/json")
        authors = Author.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(authors), 6)

    def test_delete_author(self):
        """
        Test delete author.
        """
        response = self.client.delete(self.url+str(self.author1.id)+'/', format='json')
        self.assertEqual(response.status_code, 204)