from django.contrib import admin

from django_jalali.admin.filters import JDateFieldListFilter

from .models import NewsLetter, ProductCategory, Product, IPAddress, ShoppingCart, ContactUs


class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'create_date']
    list_filter = [('create_date', JDateFieldListFilter)]

    class Meta:
        model = NewsLetter

admin.site.register(NewsLetter, NewsLetterAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'main_cat']
    ordering = ['title']

    class Meta:
        model = ProductCategory

admin.site.register(ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'product_img_tag', 'category_to_str', 'status', 'staff_amount',
                    'create_date', 'update_date']
    list_filter = [('create_date', JDateFieldListFilter)]
    ordering = ['-status', 'create_date']


    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)

admin.site.register(IPAddress)

class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['user_ip', 'product', 'count', 'date_added']

    class Meta:
        model = ShoppingCart

admin.site.register(ShoppingCart, ShoppingCartAdmin)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'message', 'send_date']

    class Meta:
        model = ContactUs

admin.site.register(ContactUs, ContactUsAdmin)