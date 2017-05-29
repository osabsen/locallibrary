from django.shortcuts import render
import nltk, re, pprint, csv, sqlite3
from nltk import word_tokenize
from urllib import request


from .models import Book, Author, BookInstance, Genre
from .ai_grammar import *
from .forms import nltkform
def index(request, *text_input):

    nltk= ["a"]
    if request.method == 'POST':
        form = nltkform(request.POST)
        if form.is_valid():
            text_input=form.cleaned_data['text_input']
    else: text_input=""
    global lines
    nltk0  = ai_grammar(text_input)
    nltk=[list(i) for i in zip(*nltk0)]
    #print(nltk)
    # Render the HTML template index.html with the data in the context variable
    return render( request, 'index.html', context={'nltk':nltk}, )









from django.views import generic

class BookListView(generic.ListView):
    model = Book

class BookDetailView(generic.DetailView):
    model = Book







from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

from .forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)
    
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        
        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})
    
    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})


