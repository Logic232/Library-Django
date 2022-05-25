import django
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from base.forms import BookForm, CustomerForm, EditCustomerForm, PasswordChangingForm
from .models import Author, Books, Loans, Publisher
from django.contrib.auth.views import PasswordChangeView


# Create your views here.

def loginPage(request):
    page = 'login'
    user_check = False
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        try:
            username = request.POST.get('username').lower()
            password = request.POST.get('password')
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                user_check = True
        except:
            user_check = True

    context = {'page': page, 'user_check': user_check}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = CustomerForm()
    name_check = False
    password_check = False
    weak_password = False

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            if User.objects.filter(username=user.username).exists():
                name_check = True
            else:
                user.save()
                login(request, user)
                return redirect('home')
        else:
            if User.objects.filter(username=form["username"].value()).exists():
                name_check = True
            elif form["password1"].value() != form["password2"].value():
                password_check = True
            else:
                weak_password = True

    return render(request, 'base/login_register.html', {'form': form, 'name_check': name_check, 'password_check': password_check, 'weak_password': weak_password})


def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    books = Books.objects.filter(
        Q(book_name__icontains=q) |
        Q(book_isbn__icontains=q) |
        Q(book_edition__icontains=q) |
        Q(author_name__author_name__icontains=q) |
        Q(publisher_name__publisher_name__icontains=q)
    )

    context = {'books': books}

    return render(request, 'base/home.html', context)


def homeSec(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    books = Books.objects.filter(
        Q(book_name__icontains=q) |
        Q(book_isbn__icontains=q) |
        Q(book_edition__icontains=q) |
        Q(author_name__author_name__icontains=q) |
        Q(publisher_name__publisher_name__icontains=q)
    )
    context = {'books': books}

    return render(request, 'base/home_sec.html', context)


def book(request, pk):
    book = Books.objects.get(book_name=pk)
    book_name = book.book_name
    book_edition = book.book_edition
    book_author = book.author_name
    book_publisher = book.publisher_name
    book_isbn = book.book_isbn
    book_year = book.book_year
    book_link = book.book_link
    book_loan = list(Books.objects.filter(
        book_name=pk).values_list('loan_id', flat=True))
    del_or_upd = None
    #book_loan = book.values_list('Loans', flat=True)

    if request.method == 'POST' and 'loan' in request.POST:
        loan = Loans.objects.get(id=book_loan[0])
        if loan.loan_is_active == False:
            loan.loan_is_active = True
            loan.user_name = request.user
            loan.save()
            return redirect('loans-user')
        else:
            return redirect('book', pk=book_name)

    if request.method == 'POST' and 'update' in request.POST:
        loan = Loans.objects.get(id=book_loan[0])
        if loan.loan_is_active == False:
            return redirect('update-book', pk=book_name)
        else:
            del_or_upd = True

    # if request.method == 'POST' and 'delete' in request.POST:

    if request.method == 'POST' and 'check' in request.POST:
        loan = Loans.objects.get(id=book_loan[0])
        if loan.loan_is_active == False:
            loan.delete()
            return redirect('home')
        else:
            del_or_upd = True

    context = {'book': book, 'book_name': book_name, 'book_edition': book_edition,
               'book_author': book_author, 'book_publisher': book_publisher, 'book_isbn': book_isbn, 'book_loan': book_loan, 'del_or_upd': del_or_upd, 'book_link': book_link, 'book_year': book_year}
    return render(request, 'base/book.html', context)


def updateBook(request, pk):

    book = Books.objects.get(book_name=pk)
    form = BookForm()
    authors = Author.objects.all()
    publishers = Publisher.objects.all()

    if request.method == 'POST':
        form = BookForm(request.POST)

        author_name = request.POST.get('author')
        publisher_name = request.POST.get('publisher')
        author, created = Author.objects.get_or_create(author_name=author_name)
        publisher, created = Publisher.objects.get_or_create(
            publisher_name=publisher_name)

        Books.objects.filter(book_name=pk).update(
            book_name=request.POST.get('book_name'),
            book_year=request.POST.get('book_year'),
            book_isbn=request.POST.get('book_isbn'),
            book_edition=request.POST.get('book_edition'),
            book_link=request.POST.get('book_link'),
            author_name=author,
            publisher_name=publisher
        )
        book = Books.objects.get(book_name=request.POST.get('book_name'))
        return redirect('book', pk=book.book_name)

    context = {'book': book, 'form': form,
               'authors': authors, 'publishers': publishers}
    return render(request, 'base/update-book.html', context)


@login_required(login_url='/login')
def addBook(request):
    form = BookForm()
    authors = Author.objects.all()
    publishers = Publisher.objects.all()

    if request.method == 'POST':
        test_book_name = request.POST.get('book_name')
        test_variable = list(Books.objects.filter(
            book_name=test_book_name).values_list('book_name', flat=True))

        if test_book_name in test_variable:
            return redirect('home')
        else:
            author_name = request.POST.get('author')
            publisher_name = request.POST.get('publisher')
            author, created = Author.objects.get_or_create(
                author_name=author_name)
            publisher, created = Publisher.objects.get_or_create(
                publisher_name=publisher_name)

            try:
                loans = Loans.objects.latest('id').id
                print(loans)
                temp_var = str(loans)
                loans_id = 1 + int(temp_var)
            except:
                loans_id = 1

            loans_id_create = Loans.objects.create(id=loans_id)
            Books.objects.create(
                book_name=request.POST.get('book_name'),
                book_year=request.POST.get('book_year'),
                book_isbn=request.POST.get('book_isbn'),
                book_edition=request.POST.get('book_edition'),
                book_link=request.POST.get('book_link'),
                author_name=author,
                publisher_name=publisher,
                loan_id=loans_id_create
            )
            return redirect('home')

    context = {'form': form, 'authors': authors,
               'publishers': publishers}
    return render(request, 'base/book_form.html', context)


@login_required(login_url='/login')
def userProfile(request):
    current_user = request.user
    loans = Loans.objects.all().select_related('user_name', 'books').filter(
        user_name=current_user.id).filter(loan_is_active=True)
    last_loan = loans[0:1]
    number_of_loans = loans.count()

    context = {'loans': loans, 'last_loan': last_loan,
               'number_of_loans': number_of_loans}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = EditCustomerForm(instance=user)

    if request.method == 'POST' and 'update' in request.POST:
        form = EditCustomerForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            user = request.user
            return redirect('user-profile')

    return render(request, 'base/update-user.html', {'form': form})


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm


@login_required(login_url='login')
def loansUser(request):
    current_user = request.user
    loans = Loans.objects.all().select_related('user_name', 'books').filter(
        user_name=current_user.id).filter(loan_is_active=True)
    loan_submit = None
    #loans = user.loans_set.all()
    print(loans)

    admin_loans = Books.objects.all().select_related(
        'loan_id').filter(loan_id__loan_is_active=True)
    print(admin_loans)

    if request.method == 'POST' and 'loan' in request.POST:
        loan_submit = request.POST["loan"]

    if request.method == 'POST' and 'check' in request.POST:
        loan_id_del = request.POST["check"]
        loan_del = Loans.objects.get(id=loan_id_del)
        loan_del.loan_is_active = False
        loan_del.save()
        return redirect('loans-user')

    context = {'current_user': current_user, 'loans': loans,
               'admin_loans': admin_loans, 'loan_submit': loan_submit}

    return render(request, 'base/loans.html', context)


def server_error(request, exception=None):
    return render(request, 'base/500.html')


def page_not_found(request, exception=None):
    return render(request, 'base/404.html')


def permission_denied(request, exception=None):
    return render(request, 'base/403.html')


def bad_request(request, exception=None):
    return render(request, 'base/400.html')
