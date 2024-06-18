from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.decorators import login_required
from . import forms
from . import models
from django.contrib import messages
from user.models import AcountModel
from book.models import BorrowModel
import datetime


# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = forms.RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'User created Successfully')
            return redirect('home')
    else:
        form = forms.RegisterUserForm()
    return render(request,'register.html',{'form': form})

class UserLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Login successful')
        return super().form_valid(form)
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'Logout successful')
        return super().dispatch(request, *args, **kwargs)

@login_required 
def deposit_money(request):
    if request.method == 'POST':
        form = forms.DepositForm(request.POST)
        if form.is_valid():

            amount = form.cleaned_data.get('amount')
            try:
                user_acount = models.AcountModel.objects.get(user=request.user)
            except models.AcountModel.DoesNotExist:
                user_acount = models.AcountModel(user=request.user, balance=0)
            user_acount.balance+=amount
            user_acount.save()
            messages.success(request,f'Successfully added amount {amount}, your current balance is {user_acount.balance}')
            subject = 'DEPOSIT'
            message = f'Successfully added amount {amount} at {datetime.datetime.now()}, your current balance is {user_acount.balance} '
            from_email = settings.EMAIL_HOST_USER
            to = request.user.email
            send_mail(subject,message,from_email,[to])
            return redirect('home')
    else:
        form = forms.DepositForm()
    return render(request,'deposit.html',{'form':form})

@login_required 
def profile(request):
    books = BorrowModel.objects.filter(user=request.user)
    print(books)
    return render(request,'profile.html',{'books': books})


def account_balance(request):
    if request.user.is_authenticated:
        try:
            account = AcountModel.objects.get(user=request.user)
            return {'account_balance': account.balance}
        except AcountModel.DoesNotExist:
            return {'account_balance': 0}
    return {'account_balance': None}