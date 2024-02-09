from django.utils import timezone

from .models import IPAddress, ShoppingCart

class SaveIPAddressMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress.objects.create(ip_address=ip)

        request.user.ip_address = ip_address

        response = self.get_response(request)

        return response
    


class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_str = request.session.get('current_time')
        user_ip = request.session.get('temp_user')
        if time_str is not None:
            time_obj = timezone.datetime.strptime(time_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
            now_str = str(timezone.now()).split('.')[0]
            time_diff = timezone.datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S') - time_obj
            if time_diff.seconds > 86400:  # 1 day
                del request.session['current_time']
                del request.session['temp_user']
                ShoppingCart.objects.filter(user_ip__ip_address=user_ip).delete()
                IPAddress.objects.filter(ip_address=user_ip).delete()

        response = self.get_response(request)
        return response



