from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    author_name = models.CharField(max_length=50)

    def __str__(self):
        return self.author_name

class Publisher(models.Model):
    publisher_name = models.CharField(max_length=50)

    def __str__(self):
        return self.publisher_name

class Loans(models.Model):
    loan_date = models.DateTimeField(auto_now=True)
    loan_date_created = models.DateTimeField(auto_now_add=True)
    loan_is_active = models.BooleanField(default=False, null=True)
    user_name = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) 

    class Meta:
        ordering = ['-loan_date', '-loan_date_created']   



class Books(models.Model):
    book_name = models.CharField(max_length=50)
    book_isbn = models.CharField(max_length=20)
    book_edition = models.CharField(max_length=20, null=True)
    author_name = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher_name = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    loan_id = models.OneToOneField(Loans, on_delete=models.CASCADE, blank=True)


