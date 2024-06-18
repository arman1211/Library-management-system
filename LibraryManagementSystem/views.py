from typing import Any
from django.shortcuts import render,redirect
from book.models import BookModel,ReviewModel,BorrowModel
from user.models import AcountModel
from book.forms import ReviewForm
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from book import constrant
import datetime

def home(request,category=None):
    is_filter=False
    if category is not None:
        is_filter = True
        books = BookModel.objects.filter(category=category)
    else:
        books = BookModel.objects.all()
    if request.user.is_authenticated:
        # acount = AcountModel.objects.get(user= request.user)
        return render(request,'home.html',{'books': books,'categories': constrant.Book_Category ,'is_filter': is_filter})
    return render(request,'home.html',{'books': books,'categories': constrant.Book_Category,'is_filter': is_filter})



def buy_book(request,id):
    book = BookModel.objects.get(pk=id)
    try:
        acount = AcountModel.objects.get(user=request.user)
        BorrowModel.objects.create(user = request.user,book=book)
    except:
        acount = AcountModel.objects.create(user = request.user)
        BorrowModel.objects.create(user = request.user,book=book)
    if acount.balance >= book.borrow_price:
        acount.balance-=book.borrow_price
        acount.save()
        messages.success(request,f'succesfully borrowed {book.title}. Your current balance is {acount.balance}')
        return redirect('profile')
    else:
        messages.warning(request,f'insufficient amount. please deposit first')
        return redirect('home')
    
def return_book(request,id):
    book = BookModel.objects.get(pk=id)
    acount = AcountModel.objects.get(user = request.user)
    borrow = BorrowModel.objects.get(user=request.user,book=book,returned=False)
    borrow.return_date = datetime.datetime.now()
    borrow.returned = True
    acount.balance += book.borrow_price
    acount.save()
    borrow.save()
    messages.success(request,f'Book returned succesfully.${book.borrow_price} has added to you acount')
    return redirect('profile')


    

class DetailBookView(FormMixin,DetailView):
    model = BookModel
    form_class = ReviewForm
    template_name = 'details.html'
    context_object_name = 'book'
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            form = self.get_form()
            context['form'] = form
        context['reviews'] = ReviewModel.objects.filter(book=self.object)
        context['is_borrowed'] = BorrowModel.objects.filter(book=self.object,user=self.request.user)
        return context
    def post(self,request,*args,**kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            review = form.save(commit = False)
            review.book = self.object
            review.user = request.user
            review.save()
            messages.success(request,'review successfull')
            return redirect('home')
            
    
