from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpRequest
from django.urls import reverse, reverse_lazy
from django.db.models import Avg, Max, Min
from django.template import loader
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from recycle_app.models import *
from datetime import datetime, timedelta, date
import time
import random

# Create your views here.
# def Alldata(request):
#     allData = Users.objects.all().values()
    
#     template = loader.get_template('readDatabase.html')
    
#     context = {
#         'query': allData,
#     }
#     return HttpResponse(template.render(context, request))

def index(request):
    if 'member_id' in request.session: #Check if user is logged in
        UID = request.session['member_id']
        if 'all' in request.GET:
            BinsInfo = Bins.objects.all().order_by('id').distinct()
        else:
            BinsInfo = Bins.objects.filter(associated=1).order_by('id').distinct()
        Userinfo = Users.objects.filter(id=UID).values()
        
        paginator = Paginator(BinsInfo, 3)
        page_number = request.GET.get('page')
        page_Bins = paginator.get_page(page_number)
        
        template = loader.get_template('index.html')
        context = {
            'page_Bins': page_Bins,
            'Userinfo': Userinfo,
        }
        return HttpResponse(template.render(context, request))
    else:
        if 'all' in request.GET:
            BinsInfo = Bins.objects.all().order_by('id').distinct()
        else:
            BinsInfo = Bins.objects.filter(associated=1).order_by('id').distinct()
        
        paginator = Paginator(BinsInfo, 3)
        page_number = request.GET.get('page')
        page_Bins = paginator.get_page(page_number)
        
        template = loader.get_template('index.html')
        context = {
            'page_Bins': page_Bins,
        }
        return HttpResponse(template.render(context, request))

def register(request):
    return render(request, 'register.html')

def add_register(request):
    if request.method == "POST":
        PN = request.POST['phone_number']
        P = request.POST['password']
        CP = request.POST['confpw']
        check_number = PN.isdigit()
        Userinfo = Users.objects.values()
        DB_UN = Userinfo.values_list('phone_number', flat=True)
        if check_number != True:
            messages.error(request, 'Phone number is not valid')
            return HttpResponseRedirect(reverse('register'))
        elif CP != P: #Check the password and confirm password is the same
            messages.error(request, 'Password and Confirm Password does not match, Please try again.')
            return HttpResponseRedirect(reverse('register'))
        elif PN in DB_UN:
            messages.error(request, 'There is already an existing account, Please try a different phone number.')
            return HttpResponseRedirect(reverse('register'))
        else:
            hashedP = make_password(P)
            insertData = Users(phone_number=PN, 
                               password=hashedP)
            insertData.save()
            member = Users.objects.get(phone_number=PN)
            request.session['member_id'] = member.id
            request.session['phone_number'] = member.phone_number
            request.session['session_time_expiry'] = time.time() + 259200 # 3 days
            messages.success(request, 'account created')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('register'))

def Login(request):
    return render(request, 'login.html')
 
def check_login(request):
    if request.method == "POST":
        PN = request.POST['phone_number']
        P = request.POST['password']
        user = Users.objects.filter(phone_number=PN).count()
        if user == 1:
            member = Users.objects.get(phone_number=PN)
            checkP = check_password(P, member.password)
            if checkP == True:
                request.session['member_id'] = member.id
                request.session['phone_number'] = member.phone_number
                request.session['session_time_expiry'] = time.time() + 259200 # 3 days
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, 'Invalid credential, Please try again')
                return HttpResponseRedirect(reverse('login'))
        else:
            messages.error(request, 'Invalid credential, Please try again')
            return HttpResponseRedirect(reverse('login'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('login'))
    
def Logout(request):
    if 'member_id' in request.session: #Check if user is logged in
        try:
            del request.session['member_id']
            request.session.clear_expired()
            return HttpResponseRedirect(reverse('index'))
        except KeyError:
            messages.error(request, 'Something went wrong try again')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'session timed out, Please login')
        return HttpResponseRedirect(reverse('index'))
    
def search(request):
    Searching = request.GET['searching']
    searchdata = Bins.objects.filter(bin_name__icontains=Searching)
    searchdata_count = Bins.objects.filter(bin_name__icontains=Searching).count()
    
    paginator = Paginator(searchdata, 3)
    page_number = request.GET.get('page')
    page_searches = paginator.get_page(page_number)
    
    if searchdata_count > 0:
        template = loader.get_template('search.html')
        context = {
            'page_searches': page_searches,
            'Searching': Searching,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'No such bins are found')
        return render(request, 'search.html')

def appointment(request):
    if 'member_id' in request.session: #Check if user is logged in
        session_id = request.session['member_id']
        DateSlots = Available_Slots.objects.values('Date').filter(Availabilty=False).distinct()
        User_DateSlots = Appoinments.objects.filter(user_id_id=session_id).values()
        User_DateSlots_count = Appoinments.objects.filter(user_id_id=session_id).count()
    
        paginator = Paginator(User_DateSlots, 3)
        page_number = request.GET.get('page')
        page_bookings = paginator.get_page(page_number)
        
        template = loader.get_template('appointment.html')
        context = {
            'user_id': session_id,
            'DateSlots': DateSlots,
            'page_bookings': page_bookings,
            'User_DateSlots_count': User_DateSlots_count,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'Please Login to access this feature!')
        return render(request, 'index.html')
    
def appointment_Timeslots(request, Date):
    if request.method == "GET":
        Slots = Available_Slots.objects.filter(Date = Date).values('available_timeslots').filter(Availabilty=False)
        return JsonResponse({ 'data' : list(Slots) })
    return HttpResponse('Wrong request')
        
        
def add_appointment(request):
    if request.method == "POST":
        UID = request.session['member_id']
        Type = request.POST['recycle_type']
        Weight = request.POST['recycle_weight']
        address = request.POST['recycle_address']
        PD = request.POST['pick_date']
        PT = request.POST['pick_time']
        
        Userinfo = Appoinments.objects.values()
        DB_PD = Userinfo.values_list('pick_up_date', flat=True)
        DB_PT = Userinfo.values_list('pick_up_time', flat=True)
        check_PD = datetime.strptime(PD, "%Y-%m-%d")
        if PD in DB_PD:
            messages.error(request, 'This date is taken, please pick another one')
            return HttpResponseRedirect(reverse('appointment'))
        elif check_PD < datetime.now():
            messages.error(request, 'The date must be after today!')
            return HttpResponseRedirect(reverse('appointment'))
        elif PT in DB_PT:
            messages.error(request, 'This timeslot is taken, please pick another one')
            return HttpResponseRedirect(reverse('appointment'))
        else:
            insertData = Appoinments(user_id_id=UID, 
                                     pick_up_date=PD,
                                     pick_up_time=PT,
                                     type = Type,
                                     weight = Weight,
                                     pick_up_address=address,)
            insertData.save()
            Available_Slots.objects.filter(Date=PD).filter(available_timeslots=PT).update(Availabilty=True)
            messages.success(request, 'Appoinment created')
            return HttpResponseRedirect(reverse('appointment'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def profile(request, phone_number=None):
    if 'member_id' in request.session: #Check if user is logged in
        User_number = phone_number
        UID = request.session['member_id']
        Userinfo = Users.objects.filter(phone_number=User_number).values()
        Redeemed_V_info = Reedemed_Vouchers.objects.filter(user_id_id=UID).filter(Usability=1).values()
        Redeemed_V_count = Reedemed_Vouchers.objects.filter(user_id_id=UID).filter(Usability=1).count()
        
        paginator = Paginator(Redeemed_V_info, 3)
        page_number = request.GET.get('page')
        page_V = paginator.get_page(page_number)
        
        template = loader.get_template('profile.html')
        context = {
            'Userinfo': Userinfo,
            'page_V': page_V,
            'Redeemed_V_count': Redeemed_V_count,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'Please Login to access this feature!')
        return render(request, 'index.html')
    
def update_profile(request, id=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            U_ID = id
            edit_ph = request.POST['user_ph']
            edit_email = request.POST['edit_email']
            Userinfo = Users.objects.exclude(id=U_ID)
            DB_UN = Userinfo.values_list('email', flat=True)
            try:
                validate_email(edit_email)
            except ValidationError as e:
                messages.error(request, "Please try an accepted email format", e)
                url = reverse('profile', kwargs={'phone_number': edit_ph})
                return HttpResponseRedirect(url)
            
            if edit_email in DB_UN:
                messages.error(request, 'There is already an existing email, Please try a different email.')
                url = reverse('profile', kwargs={'phone_number': edit_ph})
                return HttpResponseRedirect(url)
            else:
                Users.objects.filter(id=U_ID).update(email=edit_email)
                messages.success(request, 'Email updated!')
                url = reverse('profile', kwargs={'phone_number': edit_ph})
                return HttpResponseRedirect(url)
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def del_profile(request, id=None):
    if request.method == "POST":
        if 'member_id' in request.session: #Check if user is logged in
            ID = id
            Users.objects.filter(id=ID).delete()
            Appoinments.objects.filter(user_id_id=ID).delete()
            Reedemed_Vouchers.objects.filter(user_id_id=ID).delete()
            del request.session['member_id']
            request.session.clear_expired()
            messages.success(request, 'account deleted')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'session timed out, Please login')
            return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('index'))
    
def voucher(request):
    if 'member_id' in request.session: #Check if user is logged in
        UID = request.session['member_id']
        Userinfo = Users.objects.filter(id=UID).values()
        Voucherinfo = Available_Vouchers.objects.all().values()
        
        template = loader.get_template('voucher.html')
        context = {
            'Userinfo': Userinfo,
            'Voucherinfo': Voucherinfo,
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'Please Login to access this feature!')
        return render(request, 'index.html')
    
def add_voucher(request):
    if request.method == "POST":
        UID = request.POST['userID']
        Type = request.POST['Type']
        Discount = request.POST['Discount']
        Cost = int(request.POST['Cost'])
        Point_info = Users.objects.filter(id=UID).aggregate(points=Max('points'))
        Pointinfo = Point_info.get('points', 1)
        if Cost > Pointinfo:
            messages.error(request, 'You do not have enough points')
            return HttpResponseRedirect(reverse('voucher'))
        else:
            Code = random.randint(1000000000, 9999999999)
            while Reedemed_Vouchers.objects.filter(Code=Code):
                Code = random.randint(1000000000, 9999999999)
            print(date.today())
            Expire = date.today() - timedelta(days=30)
            Resulting_points = Pointinfo - Cost
            insertData = Reedemed_Vouchers(Type=Type,
                                           Code=Code,
                                           exp_date=Expire,
                                           user_id_id=UID, 
                                           Discount=Discount)
            insertData.save()
            Users.objects.filter(id=UID).update(points=Resulting_points)
            messages.success(request, 'Voucher reedemed! Please check your profile for the code.')
            return HttpResponseRedirect(reverse('voucher'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('voucher'))

def FP_em_ph(request):
    return render(request, 'FP_email.html')

def FP_OTP(request):
    if request.method == "POST":
        method = request.POST['FP_Method']
        if method == "phone_number":
            PN = request.POST['phone_number']
            check_number = PN.isdigit()
            user_ph = Users.objects.filter(phone_number=PN).count()
            if check_number != True:
                messages.error(request, 'Phone number is not valid')
                return HttpResponseRedirect(reverse('forget'))
            elif user_ph == 1:
                userinfo = Users.objects.filter(phone_number=PN).values()
                OTP = random.randint(10000000, 99999999)
                template = loader.get_template('FP_OTP.html')
                context = {
                    'OTP': OTP,
                    'method': method,
                    'userinfo': userinfo,
                }
                return HttpResponse(template.render(context, request))
            else:
                messages.error(request, 'This Phone number is not found')
                return HttpResponseRedirect(reverse('forget'))
        elif method == "email":
            EM = request.POST['email']
            try:
                validate_email(EM)
            except ValidationError as e:
                messages.error(request, "Please try an accepted email format", e)
                return HttpResponseRedirect(reverse('forget'))
            user_em = Users.objects.filter(email=EM).count()
            if user_em == 1:
                userinfo = Users.objects.filter(email=EM).values()
                OTP = random.randint(10000000, 99999999)
                template = loader.get_template('FP_OTP.html')
                context = {
                    'OTP': OTP,
                    'method': method,
                    'userinfo': userinfo,
                }
                return HttpResponse(template.render(context, request))
            else:
                messages.error(request, 'This email is not found')
                return HttpResponseRedirect(reverse('forget'))

    else:
        messages.error(request, 'Please do the procedure step by step')
        return HttpResponseRedirect(reverse('forget'))

def FP_update(request):
    if request.method == "POST":
        OTP = request.POST['OTP']
        cfw_OTP = request.POST['cfw_OTP']
        method = request.POST['method']
        user_id = request.POST['user_id']

        if OTP != cfw_OTP: #Check the OTP and confirm OTP is the same
            messages.error(request, 'OTP does not match, Please try again.')
            return HttpResponseRedirect(reverse('forget'))
        
        template = loader.get_template('FP_update.html')
        context = {
            'method': method,
            'user_id': user_id,
        }
       
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, 'Please do the procedure step by step')
        return HttpResponseRedirect(reverse('forget'))

def FP_updating(request):
    if request.method == "POST":
        method = request.POST['method']
        userID = request.POST['user_id']
        P = request.POST['password']
        CP = request.POST['confpw']
        
        Userinfo = Users.objects.values()
        DB_UN = Userinfo.values_list('phone_number', flat=True)
        if CP != P: #Check the password and confirm password is the same
            messages.error(request, 'Password and Confirm Password does not match, Please try again.')
            return HttpResponseRedirect(reverse('forget'))
        else:
            hashedP = make_password(P)
            Users.objects.filter(id=userID).update(password=hashedP)
            messages.success(request, 'password updated!')
            return HttpResponseRedirect(reverse('login'))
    else:
        messages.error(request, 'Do not access these url directly')
        return HttpResponseRedirect(reverse('forget'))
    
def FAQ(request):
    return render(request, 'FAQ.html')