from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Book, BookInstance, Author

@login_required
def index(request):
    # Generate count of all the books
    number_of_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()

    # Authors
    num_authors = Author.objects.count()

    # Number of time you have visited this page
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': number_of_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    }

    return render(request, 'catalogue/index.html', context=context)


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 2

    # def get_queryset(self):
    #     #  Five books containing the title war
    #     return Book.objects.filter(title_icontains='war')[:5]

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context["some_data"] = 'This is just some dat'
    #     return context


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author
