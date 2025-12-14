from django.shortcuts import render

from data.Wrappers import (
    log,
    safe_log
)


@safe_log
def home(request):
    return render(request, 'BrowserModule/home.html', content_type="text/html")


@log
def about(request):
    return render(request, 'about.html', content_type="text/html")


@log
def add_book_handler(request):
    pass


@log
def remove_book_handler(request):
    pass


@log
def see_read_books_handler(request):
    pass
