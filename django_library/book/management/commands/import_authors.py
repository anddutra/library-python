import csv
from django.core.management.base import BaseCommand, CommandError
from book.models import Author

class Command(BaseCommand):
    help = "Import csv file with authors' name."

    def add_arguments(self, parser):
        parser.add_argument("csv_file", help="csv file with authors' name", type=open)

    def handle(self, *args, **options):
        
        try:
            csv_file = csv.DictReader(options["csv_file"])
            authors = [Author(name=row['name']) for row in csv_file]
            result = Author.objects.bulk_create(authors)
        except:
            self.stderr.write("Error to import file!")
        else:
            self.stdout.write(f'{len(result)} authors imported successfully!')