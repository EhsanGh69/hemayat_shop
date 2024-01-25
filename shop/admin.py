from django.contrib import admin

from django_jalali.admin.filters import JDateFieldListFilter

from .models import NewsLetter


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_date']
    list_filter = [('create_date', JDateFieldListFilter)]

    class Meta:
        model = NewsLetter

admin.site.register(NewsLetter, NewsLetterAdmin)
