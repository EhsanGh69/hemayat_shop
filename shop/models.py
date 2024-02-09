from django.db import models
from django.utils.html import format_html

from django_jalali.db import models as jmodels
from jdatetime import datetime





class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس آی پی')

    def __str__(self):
        return self.ip_address



class ProductCategory(models.Model):
    MAIN_CATS = (
        ('hc', 'صنایع دستی'),
        ('fs', 'مواد غذایی'),
        ('ha', 'لوازم خانگی'),
        ('rt', 'تفریح و گردشگری')
    )
    main_cat = models.CharField(max_length=2, choices=MAIN_CATS, verbose_name='گروه')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته‌بندی')

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.title
    
    def get_slug(self):
        return self.title.replace(' ', '-')



def products_image_path(instance, filename):
    file_ext = filename.split('.')[-1]
    time_str = str(datetime.now().time()).split('.')[0].replace(':', '_')
    return f"products_images/{instance.title}_{time_str}.{file_ext}"


class Product(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان محصول')
    price = models.PositiveIntegerField(default=0, verbose_name='قیمت')
    desc = models.TextField(null=True, blank=True, verbose_name='توضیحات')
    product_img = models.ImageField(upload_to=products_image_path, verbose_name='تصویر')
    category = models.ForeignKey(ProductCategory, null=True, on_delete=models.SET_NULL, related_name='products', verbose_name='دسته بندی')
    status = models.BooleanField(default=True, verbose_name='وضعیت موجودی')
    staff_amount = models.PositiveIntegerField(default=0, verbose_name='تعداد موجودی')
    create_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    update_date = jmodels.jDateTimeField(auto_now=True, verbose_name='زمان آخرین ویرایش')

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.title
    
    def get_slug(self):
        return self.title.replace(' ', '-')
    
    def product_img_tag(self):
        return format_html(f"<img src='{self.product_img.url}' width='100' height='75' style='border-radius: 5px;'>")
    product_img_tag.short_description = "تصویر محصول"

    def category_to_str(self):
        main_cat = ''
        if self.category.main_cat == 'hc':
            main_cat = 'صنایع دستی'
        elif self.category.main_cat == 'fs':
            main_cat = 'مواد غذایی'
        elif self.category.main_cat == 'ha':
            main_cat = 'لوازم خانگی'
        else:
            main_cat = 'تفریح و گردشگری'
        return f"{main_cat} / {self.category.title}"
    category_to_str.short_description = "دسته‌بندی"



class ShoppingCart(models.Model):
    user_ip = models.ForeignKey(IPAddress, on_delete=models.CASCADE, verbose_name='آی پی کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    count = models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')
    date_added = jmodels.jDateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "محصول سبد خرید"
        verbose_name_plural = "سبد خرید"

    def __str__(self):
        return f'{self.user_ip.ip_address}:{self.product.title}'

    def get_total_price(self):
        return self.product.price * self.count



def news_image_path(instance, filename):
    file_ext = filename.split('.')[-1]
    time_str = str(datetime.now().time()).split('.')[0].replace(':', '_')
    return f"news_images/{time_str}.{file_ext}"
    

class NewsLetter(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان خبر')
    content = models.TextField(verbose_name='متن خبر')
    author = models.CharField(max_length=250, null=True, blank=True, verbose_name='نویسنده خبر')
    news_img = models.ImageField(upload_to=news_image_path, verbose_name='تصویر')
    create_date = jmodels.jDateField(auto_now_add=True, verbose_name='تاریخ انتشار')
    update_date = jmodels.jDateField(auto_now=True)

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"

    def __str__(self):
        return self.title
    
    def get_slug(self):
        return self.title.replace(' ', '-')



class ContactUs(models.Model):
    full_name = models.CharField(max_length=250, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=150, verbose_name='آدرس ایمیل')
    subject = models.CharField(max_length=100, verbose_name='موضوع')
    message = models.TextField(verbose_name='متن پیام')
    send_date = jmodels.jDateTimeField(auto_now_add=True, verbose_name='ناریخ ارسال')

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "تماس با ما"

    def __str__(self):
        return f'{self.full_name}:{self.subject}'
