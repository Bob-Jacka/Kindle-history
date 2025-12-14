from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    path('addBook/', views.add_book_handler, name='add'),
    path('removeBook/', views.remove_book_handler, name='rm'),
    path('seeReadBooks/', views.see_read_books_handler, name='see'),
]
