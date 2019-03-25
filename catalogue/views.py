from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import Book, BookInstance, Author

from .forms import RenewBookModelForm
import datetime


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


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': None}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']


class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookListView(LoginRequiredMixin, ListView):
    model = Book
    paginate_by = 2


class BookDetailView(DetailView):
    model = Book


class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Class based views for listing books on loan to the current user"""
    model = BookInstance
    template_name = 'catalogue/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class BorrowedBooksLibrarianListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Class based view for listing all borrowed books. This view is only accessible by librarians with permission
     to mark books as returned"""

    permission_required = 'catalogue.can_mark_returned'
    model = BookInstance
    template_name = 'catalogue/bookinstance_list_borrowed_librarian.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').all().order_by('due_back')

    def handle_no_permission(self):
        # add custom message
        messages.error(
            self.request, 'You have no permission to access this page')
        return super(BorrowedBooksLibrarianListView, self).handle_no_permission()


@permission_required('catalogue.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a post request, then process the form data
    if request.method == 'POST':
        # Bind the data
        form = RenewBookModelForm(request.POST)

        # is form valid?
        if form.is_valid():
            # process the data
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to new url
            return HttpResponseRedirect(reverse('all-borrowed'))

        # if it's a GET request
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookModelForm(
            initial={'due_back': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalogue/book_renew_librarian.html', context)
