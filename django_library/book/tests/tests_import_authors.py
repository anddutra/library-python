from rest_framework.test import APITestCase
from django.core import management
from book.models import Author
from io import StringIO

class TestImportAuthors(APITestCase):
    """
    Test import authors
    """
    
    def test_import_authors_valid(self):
        """
        Test import a valid file
        """
        out = StringIO()
        error = StringIO()
        management.call_command('import_authors', 'authors.csv', stdout=out, stderr=error)
        authors = Author.objects.all()

        self.assertIn('15 authors imported successfully!', out.getvalue())
        self.assertIn('', error.getvalue())
        self.assertEqual(len(authors), 15)

    def test_import_authors_invalid(self):
        """
        Test import an invalid file
        """
        out = StringIO()
        error = StringIO()
        management.call_command('import_authors', 'invalid_authors.csv', stdout=out, stderr=error)
        authors = Author.objects.all()

        self.assertIn('Error to import file!', error.getvalue())
        self.assertIn('', out.getvalue())
        self.assertEqual(len(authors), 0)