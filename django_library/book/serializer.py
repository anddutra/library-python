from rest_framework import serializers
from .models import Author, Book, AuthorBook
from rest_framework.utils import model_meta

class AuthorSerializer(serializers.ModelSerializer):
    """
    Author's serializer
    """
    class Meta:
        model = Author
        fields = '__all__'

class AuthorBookSerializer(serializers.ModelSerializer):
    """
    Author's Book serializer
    """
    author_name = serializers.CharField(read_only=True)

    class Meta:
        model = AuthorBook
        fields = ['author', 'author_name']

class BookSeralizer(serializers.ModelSerializer):
    """
    Book's serializer
    """
    authorsbook = AuthorBookSerializer(many=True)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        """
        Create book and its authors
        """
        authorsbook_data = validated_data.pop('authorsbook')
        book = Book.objects.create(**validated_data)
        for author_data in authorsbook_data:
            AuthorBook.objects.create(
                book=book, **author_data)
        return book

    def update(self, instance, validated_data):
        """
        Update book and its authors
        """
        authors_book_data = validated_data.pop('authorsbook')
        authors_book_db = AuthorBook.objects.filter(book=instance)

        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        for author_data in authors_book_data:
            is_new = True
            for author_db in authors_book_db:
                if author_data["author"] == author_db.author:
                    is_new = False
                    break
            if is_new:     
                AuthorBook.objects.create(book=instance, **author_data)

        for author_db in authors_book_db:
            is_deleted = True
            for author_data in authors_book_data:
                if author_data["author"] == author_db.author:
                    is_deleted = False
                    break
            if is_deleted:
                AuthorBook.objects.get(
                    id=author_db.id).delete()

        instance.save()
        return instance