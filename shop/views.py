from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, ListView, DeleteView, CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone

from .models import NewsLetter, Product, ProductCategory, ShoppingCart, ContactUs
from .forms import ContactUsForm


def home(request):

    news_letters = NewsLetter.objects.all()
    
    # time_str = request.session.get('current_time')
    # if time_str:
    #     time_obj = timezone.datetime.strptime(time_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
    #     now_str = str(timezone.now()).split('.')[0]
    #     time_diff = timezone.datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S') - time_obj
    #     print(time_diff.seconds)
    # else:
    #     print('session has expired!')

    

    return render(request, 'shop/home.html', { 'news_letters': news_letters })


def navbar_view(request):
    ip_obj = request.user.ip_address
    cart_count = ShoppingCart.objects.filter(user_ip=ip_obj).count()

    return render(request, 'shop/partials/navbar.html', { 'cart_count': cart_count })



def shop_cart(request):
    ip_obj = request.user.ip_address
    cart_objects = ShoppingCart.objects.filter(user_ip=ip_obj).order_by('date_added').all()
    
    if cart_objects:
        cart_objects_prices = [obj.get_total_price() for obj in cart_objects]
        total_cart_price = sum(cart_objects_prices)
        return render(request, 'shop/shop_cart.html', { 'empty_cart': False, 
                                                       'cart_objects': cart_objects, 
                                                       'total_cart_price':total_cart_price })
    return render(request, 'shop/shop_cart.html', { 'empty_cart': True })


class HandicraftsProducts(ListView):
    context_object_name = "hand_products"
    template_name = "shop/products/handicrafts_products.html"
    paginate_by = 15

    def get_queryset(self):
        category = self.request.GET.get('category')
        if category:
            return Product.objects.filter(category__title=category).order_by('-status', 'create_date').all()
        return Product.objects.order_by('-status', 'create_date').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip_obj = self.request.user.ip_address
        cart_objects = ShoppingCart.objects.filter(user_ip=ip_obj).all()
        context['cart_products'] = [obj.product for obj in cart_objects]
        context['hand_categories'] = ProductCategory.objects.filter(main_cat='hc').all()
        return context
    

class HandicraftProduct(DetailView):
    context_object_name = "hand_product"
    template_name = "shop/products/handicraft_product.html"

    def get_object(self):
        slug = self.kwargs.get('slug')
        product_title = slug.replace('-', ' ')
        return get_object_or_404(Product, title=product_title)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ip_obj = self.request.user.ip_address
        cart_objects = ShoppingCart.objects.filter(user_ip=ip_obj).all()
        context['cart_products'] = [obj.product for obj in cart_objects]
        context['hand_categories'] = ProductCategory.objects.filter(main_cat='hc').all()
        return context


def add_to_cart(request):
    ip_obj = request.user.ip_address
    temp_user = request.session.get('temp_user')
    if temp_user is None:
        request.session['current_time'] = str(timezone.now())
        request.session['temp_user'] = ip_obj.ip_address

    product_id = request.POST.get('product_id')

    product = get_object_or_404(Product, pk=product_id)

    existing_product = ShoppingCart.objects.filter(user_ip=ip_obj, product=product).first()

    if not existing_product:
        ShoppingCart.objects.create(user_ip=ip_obj, product=product)
        messages.add_message(request, messages.SUCCESS, f"{product_id}")
        

    category = request.GET.get('category')
    if category:
        return redirect(reverse_lazy('shop:handicrafts_products') + f'?category={category}')
    return redirect(reverse_lazy('shop:handicrafts_products'))


class DeleteCartProduct(DeleteView):
    success_url = reverse_lazy("shop:shop_cart")

    def get_object(self):
        obj_id = int(self.kwargs.get('pk'))
        return get_object_or_404(ShoppingCart, pk=obj_id)
    

def change_product_count(request, **kwargs):
    pk = kwargs.get('pk')
    product_cart = get_object_or_404(ShoppingCart, pk=pk)

    act = request.GET.get('act')
    if act == 'plus':
        product_cart.count += 1
        product_cart.save()
    elif act == 'minus':
        product_cart.count -= 1
        product_cart.save()
        
    return redirect(reverse_lazy('shop:shop_cart'))



class NewsLetters(ListView):
    context_object_name = "news_letters"
    template_name = "shop/news_archive.html"
    paginate_by = 6

    def get_queryset(self):
        return NewsLetter.objects.order_by('create_date').all()
    

class NewsDetail(DetailView):
    context_object_name = "news"
    template_name = "shop/news_detail.html"

    def get_object(self):
        slug = self.kwargs.get('slug')
        news_title = slug.replace('-', ' ')
        return get_object_or_404(NewsLetter, title=news_title)



class ContactUsView(SuccessMessageMixin, CreateView):
    model = ContactUs
    template_name = "shop/contact_us.html"
    form_class = ContactUsForm
    success_url = reverse_lazy("shop:contact_us")
    success_message = "پیام شما با موفقیت ارسال شد"
