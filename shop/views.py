from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from .models import NewsLetter


def home(request):

    news_letters = NewsLetter.objects.all()

    return render(request, 'shop/home.html', { 'news_letters': news_letters })


class NewsDetail(DetailView):
    context_object_name = "news"
    template_name = "shop/news_detail.html"

    def get_object(self):
        slug = self.kwargs.get('slug')
        news_title = slug.replace('-', ' ')
        return get_object_or_404(NewsLetter, title=news_title)



def shop_cart(request):

    return render(request, 'shop/shop_cart.html', {})


def news_letters(request):

    return render(request, 'shop/news_archive.html', {})


def handicrafts_products(request):

    return render(request, 'shop/handicrafts_products.html', {})


def contact_us(request):

    return render(request, 'shop/contact_us.html', {})

