from django.contrib import admin

from core.entities.browser.WebInterface.BrowserModule.models import (
    Books,
    Book_manufacturers
)

# Register your models here.

admin.site.register(Books)
admin.site.register(Book_manufacturers)
