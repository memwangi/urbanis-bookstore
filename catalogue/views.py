from django.shortcuts import render
from .models import Book, BookInstance, Author


def index(request):
    # Generate count of all the books
    number_of_books = Book.objects.all().count()
    num_instance = BookInstance.objects.count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # Authors
    num_authors = Author.objects.count()

    context = {
        'num_books': number_of_books,
        'num_instance': num_instance,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors
    }

    return render(request, 'catalogue/index.html', context=context)
