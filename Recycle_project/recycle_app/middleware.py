from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Avg, Max, Min
from recycle_app.models import *
from datetime import datetime, timedelta, date
import time

class SessiontimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs): 
        if 'member_id' in request.session:
            expires_time = request.session['session_time_expiry']
            timeleft = expires_time - time.time()
            
            if timeleft < 10:
                del request.session['member_id']
                request.session.clear_expired()
                messages.success(request, 'session timed out, Please login')
                return HttpResponseRedirect(reverse('index'))
            
class CheckExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs): 
        if 'member_id' in request.session:
            Reedemed_Vouchers.objects.filter(exp_date__lt=date.today()).update(Usability=True)