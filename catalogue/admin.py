from django.contrib import admin

from catalogue.models import Author, Genre, Book, BookInstance, Language


# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model = Book
# Define the admin class

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        ("Details", {
            "fields": ('book', 'imprint', 'id'),
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )
