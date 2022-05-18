from pyexpat import model
from django.forms import CharField, EmailField, ModelForm, PasswordInput
from .models import Books, User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "placeholder": f'{str(field)}',
                'class': "w-full h-[60px] px-5 rounded-lg text-sm"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )



class EditCustomerForm(ModelForm):
    email = EmailField()
    first_name = CharField(max_length=100)
    last_name = CharField(max_length=100)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "placeholder": f'{str(field)}',
                'class': "w-full h-[60px] px-5 rounded-lg text-sm"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )

class PasswordChangingForm(PasswordChangeForm):
    old_password = CharField(widget=PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = CharField(max_length=100, widget=PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = CharField(max_length=100, widget=PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
                "placeholder": f'{str(field)}',
                'class': "w-full h-[60px] px-5 rounded-lg text-sm"
            }
            self.fields[str(field)].widget.attrs.update(
                new_data
            )