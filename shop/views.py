from django.shortcuts import render



def home(request):

    return render(request, 'shop/home.html', {})


def shop_cart(request):

    return render(request, 'shop/shop_cart.html', {})


def news_letters(request):

    return render(request, 'shop/news_archive.html', {})


def handicrafts_products(request):

    return render(request, 'shop/handicrafts_products.html', {})


def contact_us(request):

    return render(request, 'shop/contact_us.html', {})

