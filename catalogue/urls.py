from django.urls import path, re_path
from .views import index, BookListView, BookDetailView, AuthorListView, AuthorDetailView, LoanedBooksByUserListView, BorrowedBooksLibrarianListView, renew_book_librarian


urlpatterns = [
    path('', index, name='index'),
    path('mybooks/', LoanedBooksByUserListView.as_view(), name="my-borrowed"),
    path('borrowed/', BorrowedBooksLibrarianListView.as_view(), name="all-borrowed"),
    path('books/', BookListView.as_view(), name='books'),
    re_path(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    path('author/', AuthorListView.as_view(), name='authors'),
    re_path(r'^author/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author_detail'),
    path('book/<uuid:pk>/renew/', renew_book_librarian,
         name='renew-book-librarian'),
]
