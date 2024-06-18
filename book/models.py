from django.db import models
from django.contrib.auth.models import User
from . constrant import Book_Category,ratings
# Create your models here.

class BookModel(models.Model):
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrow_price = models.IntegerField()
    category = models.CharField(max_length=20,choices=Book_Category)

class ReviewModel(models.Model):
    book = models.ForeignKey(BookModel,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    rating = models.IntegerField(choices=ratings)
    review = models.TextField()

class BorrowModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    returned = models.BooleanField(default=False)