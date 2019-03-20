from django.urls import path
from .views import index, BookListView, BookDetailView, AuthorListView, AuthorDetailView

urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path(r'^book/(?P<pk>\d+)$', BookDetailView.as_view(), name='book_detail'),
    path('author/', AuthorListView.as_view(), name='authors'),
    path(r'^author/(?P<pk>\d+)$', AuthorDetailView.as_view(), name='author_detail')
]
