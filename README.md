# Library API

## Description

Web API developed with Django framework.
This api simulates a library, where you can store authors and their books.

## Requirements

All the necessary requirements for running this API are in the requirements.txt file.

## Testing Instructions

To execute the unit tests, it's necessary to execute the command below inside the django_library folder.

```
py.exe manage.py test book/tests
```

## API

This API is published on Heroku and can be accessed at the address: https://anddutra-library.herokuapp.com/

**Author**

To create an author is necessary execute POST with this json format:
Endpoint: /authorapi/

```
{
  "name": "J. K. Rowling"
}
```

Execute a get to this endpoint to list all authors.
It is possible filter the author by name.
Example: /authorapi?search=J. K. Rowling

**Book**

To create a book is necessary execute POST with this json format:
Endpoint: /bookapi/

```
{
  "authorsbook": [
    {
      "author": 1
    }
  ],
  "name": "Harry Potter and the Philosopher’s Stone",
  "edition": 1,
  "publication_year": 1997
}
```

Execute a get to this endpoint to list all books.
It is possible filter the books by name, edition, publication_year and authors' name.
Example: /bookapi?search=Harry Potter

## Commands

It is possible to execute the command bellow inside the django_library folder to import authors in csv format.

```
python manage.py import_authors authors.csv
```

authors.csv is the name of the file containing the records to be imported.

## Work Environment

* Windows 10
* Visual Studio Code
* Python 3.7.5
* pip 19.3.1
* Django 3.0.1
* Django Rest Framwork 3.10.3