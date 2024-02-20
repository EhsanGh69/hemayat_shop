from django.urls import path

from .views import (
    home, navbar_view, shop_cart, NewsLetters, AllProducts, NewsDetail, 
    SingleProduct, add_to_cart, DeleteCartProduct, change_product_count, ContactUsView
)

app_name = "shop"

urlpatterns = [
    path('', home, name="home"),
    path('navbar_view/', navbar_view, name="navbar_view"),
    path('shop_cart/', shop_cart, name="shop_cart"),
    path('news_letters/', NewsLetters.as_view(), name="news_letters"),
    path('news_letters/page/<int:page>', NewsLetters.as_view(), name="news_letters"),
    path('news_detail/<str:slug>', NewsDetail.as_view(), name="news_detail"),
    path('products/<str:group>', AllProducts.as_view(), name="all_products"),
    path('products/<str:group>/page/<int:page>', AllProducts.as_view(), name="all_products"),
    path('products/<str:group>/<str:slug>', SingleProduct.as_view(), name="single_product"),
    path('add_to_cart/', add_to_cart, name="add_to_cart"),
    path('delete_from_cart/<int:pk>', DeleteCartProduct.as_view(), name="delete_from_cart"),
    path('change_product_count/<int:pk>', change_product_count, name="change_product_count"),
    path('contact_us/', ContactUsView.as_view(), name="contact_us"),
]
