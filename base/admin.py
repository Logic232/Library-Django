from django.contrib import admin

from .models import Author, Publisher, Books, Loans

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Books)
admin.site.register(Loans)