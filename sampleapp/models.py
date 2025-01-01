from django.db import models
from django.db.models import F, Case, When, Value

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()

    def __str__(self):
        return self.name
    
class Book(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField()
    copies = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class Borrow(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    member_name = models.CharField(max_length=100)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return self.member_name

