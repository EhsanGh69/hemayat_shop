from django.urls import path

from .views import home, shop_cart, news_letters, handicrafts_products, contact_us

app_name = "shop"

urlpatterns = [
    path('', home, name="home"),
    path('shop_cart/', shop_cart, name="shop_cart"),
    path('news_letters/', news_letters, name="news_letters"),
    path('products/handicrafts', handicrafts_products, name="handicrafts_products"),
    path('contact_us/', contact_us, name="contact_us"),
]
