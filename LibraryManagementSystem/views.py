from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.conf import settings
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


@login_required 
def buy_book(request,id):
    book = BookModel.objects.get(pk=id)
    try:
        acount = AcountModel.objects.get(user=request.user)
        
    except:
        acount = AcountModel.objects.create(user = request.user)
    if acount.balance >= book.borrow_price:
        BorrowModel.objects.create(user = request.user,book=book)
        acount.balance-=book.borrow_price
        acount.save()
        messages.success(request,f'succesfully borrowed {book.title}. Your current balance is {acount.balance}')
        subject = 'Book Borrowed Successfully'
        message = f'succesfully borrowed {book.title}. Your current balance is {acount.balance}. Your borrowing date is {datetime.datetime.now()}'
        from_email = settings.EMAIL_HOST_USER
        to = request.user.email
        send_mail(subject,message,from_email,[to])
        return redirect('profile')
    else:
        messages.warning(request,f'insufficient amount. please deposit first')
        return redirect('home')
    
@login_required    
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
    subject = 'Book Returned Successfully'
    message = f'succesfully returned {book.title}.${book.borrow_price} has added to you acount. Your current balance is {acount.balance}. Your returning date is {datetime.datetime.now()}'
    from_email = settings.EMAIL_HOST_USER
    to = request.user.email
    send_mail(subject,message,from_email,[to])
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
            try:
                context['is_borrowed']=BorrowModel.objects.filter(book = self.object,user=self.request.user)
            except:
                context['is_borrowed'] = False
        context['reviews'] = ReviewModel.objects.filter(book=self.object)
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
            return redirect('details',pk=self.object.pk)
            
    
