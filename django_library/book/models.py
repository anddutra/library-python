from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Author's class
    """
    name = models.CharField(max_length=100)

class Book(models.Model):
    """
    Book's class
    """
    name = models.CharField(max_length=100)
    edition = models.IntegerField()
    publication_year = models.IntegerField()

class AuthorBook(models.Model):
    """
    Book author's class
    One book can have many authors and one author can have many books
    """
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_fk')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='authorsbook')

    @property
    def author_name(self):
        return self.author.name