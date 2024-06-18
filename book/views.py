from django.shortcuts import render,redirect
from django.contrib import messages
from django.views.generic import FormView
from .forms import BookForm
from user.models import AcountModel

# Create your views here.

class AddBookView(FormView):
    form_class = BookForm
    template_name = 'addbook.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Book added successfully')
        return super().form_valid(form)
    
    def get_success_url(self):
        return redirect('home').url
    
