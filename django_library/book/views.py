from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Author, Book
from .serializer import AuthorSerializer, BookSeralizer

# Create your views here.
class AuthorAPI(viewsets.ModelViewSet):
    """
    ViewSet to manipulate Authors (Get, Put, Post and Delete)
    """
    queryset = Author.objects.all().order_by('id')
    serializer_class = AuthorSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name']

class BookAPI(viewsets.ModelViewSet):
    """
    ViewSet to manipulate Books and its Authors (Get, Put, Post and Delete)
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSeralizer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['name', 'publication_year', 'edition', 'authorsbook__author__name']