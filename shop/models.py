from django.db import models

from django_jalali.db import models as jmodels
from jdatetime import datetime


def get_image_path(instance, filename):
    file_ext = filename.split('.')[-1]
    time_str = str(datetime.now().time()).split('.')[0].replace(':', '_')
    return f"news_images/{time_str}.{file_ext}"
    

class NewsLetter(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان خبر')
    content = models.TextField(verbose_name='متن خبر')
    author = models.CharField(max_length=250, null=True, blank=True, verbose_name='نویسنده خبر')
    news_img = models.ImageField(upload_to=get_image_path, verbose_name='تصویر')
    create_date = jmodels.jDateField(auto_now_add=True, verbose_name='تاریخ انتشار')
    update_date = jmodels.jDateTimeField(auto_now=True)

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"

    def __str__(self):
        return self.title
    
    def get_slug(self):
        return self.title.replace(' ', '-')


