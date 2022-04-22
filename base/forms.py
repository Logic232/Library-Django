from django.forms import CharField, EmailField, ModelForm
from .models import Books, User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class BookForm(ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
        exclude = ['book_id']

class EditBookForm(ModelForm):
    book_name = CharField(max_length=50)
    book_isbn = CharField(max_length=20)
    book_edition = CharField(max_length=20)
    author_name = CharField(max_length=50)
    publisher_name = CharField(max_length=50)

    class Meta:
        model = Books
        fields = ('book_name', 'book_isbn', 'book_edition', 'author_name', 'publisher_name')

class CustomerForm(UserCreationForm):
    email = EmailField()
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditCustomerForm(ModelForm):
    email = EmailField()
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')