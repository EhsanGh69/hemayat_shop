from uuid import uuid4
from django.utils import timezone

from .models import ShoppingCart

    
class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_str = request.session.get('current_time')
        user_uuid = request.session.get('temp_user')
        if user_uuid is None and time_str is None:
            request.session['current_time'] = str(timezone.now())
            request.session['temp_user'] = str(uuid4())
        if time_str is not None:
            time_obj = timezone.datetime.strptime(time_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
            now_str = str(timezone.now()).split('.')[0]
            time_diff = timezone.datetime.strptime(now_str, '%Y-%m-%d %H:%M:%S') - time_obj
            if time_diff.seconds > 86400:  # 1 day
                del request.session['current_time']
                del request.session['temp_user']
                ShoppingCart.objects.filter(user_uuid=user_uuid).delete()

        response = self.get_response(request)
        return response



