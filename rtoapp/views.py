from random import randint

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *

from .models import *

def index(request):
    return render(request, "index_home.html")

@login_required(login_url='/admin_login/')
def dashboard(request):
    reg = Registration.objects.all()
    ll = Learning.objects.all()
    dl = Driving.objects.all()
    rto = Rto.objects.all()
    state = State.objects.all()
    city = City.objects.all()
    read = Contact2.objects.filter(status="read")
    unread = Contact2.objects.filter(status="unread")
    return render(request, "admin_dashboard.html", locals())

@login_required(login_url='/rto_login/')
def rto_dashboard(request):
    newl = Learning.objects.filter(status="Not Updated Yet", city__rto__user=request.user)
    rejectedl = Learning.objects.filter(status="Rejected", city__rto__user=request.user)
    acceptedl = Learning.objects.filter(status="Accepted", city__rto__user=request.user)
    newd = Driving.objects.filter(status="Not Updated Yet", city__rto__user=request.user)
    acceptedd = Driving.objects.filter(status="Accepted", city__rto__user=request.user)
    rejectedd = Driving.objects.filter(status="Rejected", city__rto__user=request.user)
    return render(request, "rto_dashboard.html", locals())

def mail(request):
    data = Contact.objects.all()
    d = {'data': data}
    return render(request, "mail.html", d)

def index_about(request):
    data = About.objects.all()
    d = {'data': data}
    return render(request, "index_about.html", d)

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

def admin_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        
        # Authenticate the user with the provided credentials
        user = authenticate(username=uname, password=pwd)
        
        if user:
            if user.is_staff:
                # If the user is an admin, log them in and redirect
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('dashboard')
            else:
                # If the user is not an admin
                messages.error(request, "Invalid User")
                return redirect('admin_login')
        else:
            # If the username or password is incorrect
            messages.error(request, "Invalid Username or Password")
            return redirect('admin_login')
    
    return render(request, "admin_login.html")


@login_required(login_url='/admin_login/')
def logout_admin(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('admin_login')

@login_required(login_url='/admin_login/')
def add_state(request, pid=None):
    state = None
    if pid:
        state = State.objects.get(id=pid)
    if request.method == "POST":
        state = StateForm(request.POST, request.FILES, instance=state)
        if state.is_valid():
            new_state = state.save()
            new_state.save()
        if pid:
            messages.success(request, "Update State Successful")
            return redirect('view_state')
        else:
            messages.success(request, "Add State Successful")
            return redirect('view_state')
    return render(request, 'add_state.html', locals())

@login_required(login_url='/admin_login/')
def view_state(request):
    data = State.objects.all()
    d = {'data': data}
    return render(request, "view_state.html", d)

@login_required(login_url='/admin_login/')
def delete_state(request, pid):
    data = State.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_state')

@login_required(login_url='/admin_login/')
def add_city(request, pid=None):
    city = None
    if pid:
        city = City.objects.get(id=pid)
    if request.method == "POST":
        city = CityForm(request.POST, request.FILES, instance=city)
        if city.is_valid():
            new_city = city.save()
            new_city.save()
        if pid:
            messages.success(request, "Update City Successful")
            return redirect('view_city')
        else:
            messages.success(request, "Add City Successful")
            return redirect('view_city')
    mystate = State.objects.all()
    return render(request, 'add_city.html', locals())

@login_required(login_url='/admin_login/')
def view_city(request):
    data = City.objects.all()
    d = {'data': data}
    return render(request, "view_city.html", d)

@login_required(login_url='/admin_login/')
def delete_city(request, pid):
    data = City.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_city')

@login_required(login_url='/admin_login/')
def add_rto(request, pid=None):
    stateid = request.GET.get('state', None)
    city = None
    state = None
    user = None
    rto = None
    if pid:
        user = User.objects.get(id=pid)
        rto = Rto.objects.get(user=user)
        city = City.objects.filter(state=rto.state)
    if request.method == "POST":
        form = RtoForm(request.POST, request.FILES, instance=rto)
        if form.is_valid():
            new_rto = form.save()
            if pid:
                print("hii")
                print(request.POST['firstname'], new_rto.user)
                new_rto.user.first_name = request.POST['firstname']
                new_rto.user.save()
                new_rto.save()
                messages.success(request, "RTO update successful")
                return redirect('view_rto')
            else:
                try:
                    new_user = User.objects.create_user(first_name=request.POST['firstname'], username=request.POST['username'], password=request.POST['password'])
                    new_rto.user = new_user
                    new_rto.save()
                    messages.success(request, "RTO saved successful")
                    return redirect('view_rto')
                except:
                    messages.success(request, "User already exists")
                    return redirect('add_rto')
        else:
            print(form.errors)
    mystate = State.objects.all()
    return render(request, 'add_rto.html', locals())

def city(request):
    stateid = request.GET.get('state', None)
    city = City.objects.filter(state__id=stateid)
    return render(request, 'city.html', locals())

@login_required(login_url='/admin_login/')
def view_rto(request):
    data = Rto.objects.all()
    d = {'data': data}
    return render(request, "view_rto.html", d)

@login_required(login_url='/admin_login/')
def delete_rto(request, pid):
    data = User.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_rto')

def rto_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(username=uname, password=pwd)
        if user:
            if user.is_staff:
                messages.success(request, "Invalid User")
                return redirect('rto_login')
            else:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('rto_dashboard')
        else:
            messages.success(request, "Invalid User")
            return redirect('rto_login')
    return render(request, "rto_login.html")

@login_required(login_url='/rto_login/')
def logout_rto(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('rto_login')

@login_required(login_url='/rto_login/')
def rto_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        uname = request.POST['username']
        address = request.POST['address']
        nodalname = request.POST['nodalname']


        user = User.objects.filter(id=request.user.id).update(first_name=fname, username=uname)
        Rto.objects.filter(user=request.user).update(address=address, nodalname=nodalname)
        messages.success(request, "Updation Successful")
        return redirect('rto_profile')
    data = Rto.objects.get(user=request.user)
    return render(request, "rto_profile.html", locals())

@login_required(login_url='/rto_login/')
def rto_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('rto_change_password')

    return render(request, 'rto_change_password.html')

@login_required(login_url='/admin_login/')
def admin_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('admin_change_password')

    return render(request, 'admin_change_password.html')


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistartionForm
from .models import Registration

def user_registration(request, pid=None):
    user = None
    register = None

    if pid:
        user = User.objects.get(id=pid)
        register = Registration.objects.get(user=user)

    if request.method == "POST":
        form = RegistartionForm(request.POST, request.FILES, instance=register)

        if form.is_valid():
            email = request.POST['username']  # Assuming this is your email field
            mobile = request.POST['mobile']

            # ✅ Validate 10-digit mobile number
            if not re.fullmatch(r'\d{10}', mobile):
                messages.error(request, "Mobile number must be exactly 10 digits.")
                return redirect('user_registration')

            # ✅ Check if email is already registered
            if User.objects.filter(username=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('user_registration')

            try:
                new_user = User.objects.create_user(
                    username=email,
                    email=email,
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                    password=request.POST['password']
                )
                new_register = form.save(commit=False)
                new_register.user = new_user
                new_register.save()

                messages.success(request, "Registration Successful")
                return redirect('user_login')
            except Exception as e:
                messages.error(request, f"Error during registration: {str(e)}")
                return redirect('user_registration')

    return render(request, 'user_registration.html', locals())

import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.models import User

# Function to generate a random CAPTCHA
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


def user_login(request):
    if request.method == "POST":
        uname = request.POST['username']
        pwd = request.POST['password']
        captcha_input = request.POST['captcha_input']
        captcha_session = request.session.get('captcha_code', '')

        # CAPTCHA check
        if captcha_input.strip().upper() != captcha_session:
            messages.error(request, "Invalid CAPTCHA.")
            return redirect('user_login')

        # Authentication check
        user = authenticate(username=uname, password=pwd)
        
        if user:
            if user.is_staff:
                messages.error(request, "Admin users cannot log in here.")
                return redirect('user_login')
            else:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('index')  # Redirect to homepage or dashboard
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('user_login')
    
    # On GET: generate and store a new CAPTCHA in the session
    request.session['captcha_code'] = generate_captcha()
    return render(request, 'user_login.html')

@login_required(login_url='/user_login/')
def logout_user(request):
    logout(request)
    messages.success(request, "logout Successful")
    return redirect('user_login')

@login_required(login_url='/user_login/')
def user_profile(request):
    if request.method == "POST":
        fname = request.POST['firstname']
        lname = request.POST['lastname']
        mobile = request.POST['mobile']

        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        Registration.objects.filter(user=request.user).update(mobile=mobile)
        messages.success(request, "Updation Successful")
        return redirect('user_profile')
    data = Registration.objects.get(user=request.user)
    return render(request, "user_profile.html", locals())

@login_required(login_url='/user_login/')
def user_change_password(request):
    user = User.objects.get(username=request.user.username)
    if request.method == "POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(c)
            u.save()
            messages.success(request, "Password changed successfully")
            return redirect('/')
        else:
            messages.success(request, "New password and confirm password are not same.")
            return redirect('user_change_password')

    return render(request, 'user_change_password.html')

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

@login_required(login_url='/user_login/')
def add_learning_licence(request):
    stateid = request.GET.get('name', None)
    cityobj = None
    mycity = None
    selected_state = None
    selected_city = None

    if stateid:
        stateobj = State.objects.get(id=stateid)
        mycity = City.objects.filter(state=stateobj)
        selected_state = stateobj.id

    if request.method == "POST":
        selected_state = request.POST.get('state')
        selected_city = request.POST.get('city')
        father = request.POST['father']
        birth = request.POST['birth']
        qualification = request.POST['qualification']
        licencetype = request.POST['licencetype']
        blood = request.POST['blood']
        peraddress = request.POST.get('peraddress', '')  # Optional field
        comaddress = request.POST['comaddress']
        image2 = request.FILES.get('image2')
        aadhaar_card = request.FILES.get('aadhaar_card')  # New file input
        learningnumber = random_with_N_digits(10)

        reg = Registration.objects.get(user=request.user)
        statename = State.objects.get(id=selected_state)
        cityname = City.objects.get(id=selected_city)

        Learning.objects.create(
            state=statename,
            city=cityname,
            father=father,
            register=reg,
            birth=birth,
            qualification=qualification,
            licencetype=licencetype,
            blood=blood,
            peraddress=peraddress,
            comaddress=comaddress,
            image2=image2,
            aadhaar_card=aadhaar_card,  # Save Aadhaar file
            learningnumber=learningnumber
        )

        messages.success(request, "Add Successful. Your Application No is " + str(learningnumber))
        return redirect('view_learning_licence')

    mystate = State.objects.all()
    return render(request, 'add_learning_licence.html', {
        'mystate': mystate,
        'mycity': mycity,
        'selected_state': selected_state,
        'selected_city': selected_city
    })
   

    
@login_required(login_url='/user_login/')
def edit_learning_licence(request, pid):
    stateid = request.GET.get('name', None)
    cityobj = None
    mycity = None
    if stateid:
        stateobj = State.objects.get(id=stateid)
        mycity = City.objects.filter(state=stateobj)
    if request.method == "POST":
        father = request.POST['father']
        birth = request.POST['birth']
        qualification = request.POST['qualification']
        licencetype = request.POST['licencetype']
        blood = request.POST['blood']
        peraddress = request.POST['peraddress']
        comaddress = request.POST['comaddress']
        try:
            image2 = request.FILES['image2']
            data = Learning.objects.get(id=pid)
            data.image2 = image2
            data.save()
        except:
            pass

        Learning.objects.create(father=father, birth=birth, qualification=qualification, licencetype=licencetype, blood=blood,
                                    peraddress=peraddress, comaddress=comaddress)
        messages.success(request, "Add Successful")
        return redirect('view_learning_licence')
    data = Learning.objects.get(id=pid)
    mystate = State.objects.all()
    return render(request, 'edit_learning_licence.html', locals())

@login_required(login_url='/user_login/')
def view_learning_licence(request):
    reg = Registration.objects.get(user=request.user)
    data = Learning.objects.filter(register=reg)
    d = {'data': data}
    return render(request, "view_learning_licence.html", d)

@login_required(login_url='/user_login/')
def delete_learning_licence(request, pid):
    data = Learning.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_learning_licence')

from django.contrib import messages
from django.shortcuts import render, redirect
from .models import State, City, Registration, Driving
import random

@login_required(login_url='/user_login/')
def add_driving_licence(request):
    stateid = request.GET.get('name')
    mycity = City.objects.filter(state_id=stateid) if stateid else None

    if request.method == "POST":
        name = request.POST['state']
        cityname = request.POST['city']
        father = request.POST['father']
        birth = request.POST['birth']
        qualification = request.POST['qualification']
        licencetype = request.POST['licencetype']
        blood = request.POST['blood']
        peraddress = request.POST.get('peraddress', '')  # Optional field
        comaddress = request.POST['comaddress']
        learningnumber = request.POST['learningnumber']

        image2 = request.FILES.get('image2')
        aadhaar_card = request.FILES.get('aadhaar_card')  # ✅ Aadhaar card upload

        drivingnumber = random_with_N_digits(10)

        reg = Registration.objects.get(user=request.user)
        statename = State.objects.get(id=name)
        city = City.objects.get(id=cityname)

        # ✅ Create Driving Licence object with Aadhaar card
        Driving.objects.create(
            state=statename,
            city=city,
            learningnumber=learningnumber,
            father=father,
            register=reg,
            birth=birth,
            qualification=qualification,
            licencetype=licencetype,
            blood=blood,
            peraddress=peraddress,
            comaddress=comaddress,
            image2=image2,
            drivingnumber=drivingnumber,
            aadhaar_card=aadhaar_card  # ✅ Save file field
        )

        messages.success(request, "Add Successful. Your Application No is " + str(drivingnumber))
        return redirect('view_driving_licence')

    mystate = State.objects.all()
    return render(request, 'add_driving_licence.html', locals())

@login_required(login_url='/user_login/')
def edit_driving_licence(request, pid):
    stateid = request.GET.get('name', None)
    cityobj = None
    mycity = None
    if stateid:
        stateobj = State.objects.get(id=stateid)
        mycity = City.objects.filter(state=stateobj)
    if request.method == "POST":
        father = request.POST['father']
        birth = request.POST['birth']
        qualification = request.POST['qualification']
        licencetype = request.POST['licencetype']
        blood = request.POST['blood']
        peraddress = request.POST['peraddress']
        comaddress = request.POST['comaddress']
        learningnumber = request.POST['learningnumber']
        try:
            image2 = request.FILES['image2']
            data = Learning.objects.get(id=pid)
            data.image2 = image2
            data.save()
        except:
            pass

        Driving.objects.create(learningnumber=learningnumber, father=father, birth=birth, qualification=qualification, licencetype=licencetype, blood=blood,
                                    peraddress=peraddress, comaddress=comaddress)
        messages.success(request, "Update Successful")
        return redirect('view_driving_licence')
    data = Driving.objects.get(id=pid)
    mystate = State.objects.all()
    return render(request, 'edit_driving_licence.html', locals())

@login_required(login_url='/user_login/')
def view_driving_licence(request):
    reg = Registration.objects.get(user=request.user)
    data = Driving.objects.filter(register=reg)
    d = {'data': data}
    return render(request, "view_driving_licence.html", d)

@login_required(login_url='/user_login/')
def delete_driving_licence(request, pid):
    data = Driving.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('view_driving_licence')





@login_required(login_url='/admin_login/')
def learninglist(request):
    user = request.GET.get('user')
    action = request.GET.get('action')
    data = Learning.objects.filter()
    if action == "New":
        data = data.filter(status="Not Updated Yet")
    elif action == "All":
        data = data.filter()
    elif action == "Accepted":
        data = data.filter(status="Accepted")
    elif action == "Rejected":
        data = data.filter(status="Rejected")
    if user:
        data = data.filter(register__user__id=user)
        data2 = data.filter().first()
    register = Registration.objects.filter(user=request.user)
    rto = Rto.objects.filter(user=request.user)
    if request.user.is_staff:
        return render(request, "admin_licence.html", locals())
    else:
        data = data.filter(city__rto__user=request.user)
        return render(request, "rto_learning.html", locals())

@login_required(login_url='/admin_login/')
def detail(request, pid):
    data = Learning.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        data.save()
        Trackinghistory.objects.create(learning=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('detail', pid)
    traking = Trackinghistory.objects.filter(learning=data)
    if request.user.is_staff:
        return render(request, "admin_learning_detail.html", locals())
    else:
        return render(request, "user_learning_detail.html", locals())

@login_required(login_url='/rto_login/')
def learning_detail(request, pid):
    data = Learning.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        data.save()
        Trackinghistory.objects.create(learning=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('learning_detail', pid)
    traking = Trackinghistory.objects.filter(learning=data)
    return render(request, "rto_learning_detail.html", locals())

@login_required(login_url='/admin_login/')
def drivinglist(request):
    user = request.GET.get('user')
    action = request.GET.get('action')
    data = Driving.objects.filter()
    if action == "New":
        data = data.filter(status="Not Updated Yet")
    elif action == "All":
        data = data.filter()
    elif action == "Accepted":
        data = data.filter(status="Accepted")
    elif action == "Rejected":
        data = data.filter(status="Rejected")
    if user:
        data = data.filter(register__user__id=user)
        data2 = data.filter().first()
    register = Registration.objects.filter(user=request.user)
    rto = Rto.objects.filter(user=request.user)
    if request.user.is_staff:
        return render(request, "admin_driving.html", locals())
    else:
        data = data.filter(city__rto__user=request.user)
        return render(request, "rto_driving.html", locals())

@login_required(login_url='/admin_login/')
def detail2(request, pid):
    data = Driving.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        data.save()
        Drivinghistory.objects.create(driving=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('detail2', pid)
    traking = Drivinghistory.objects.filter(driving=data)
    if request.user.is_staff:
        return render(request, "admin_driving_detail.html", locals())
    else:
        return render(request, "user_driving_detail.html", locals())

@login_required(login_url='/rto_login/')
def driving_detail(request, pid):
    data = Driving.objects.get(id=pid)
    if request.method == "POST":
        remark = request.POST['remark']
        status = request.POST['status']
        data.status = status
        data.save()
        Drivinghistory.objects.create(driving=data, remark=remark, status=status)
        messages.success(request, "Action Updated")
        return redirect('driving_detail', pid)
    traking = Drivinghistory.objects.filter(driving=data)
    return render(request, "rto_driving_detail.html", locals())

def rto_search_ll(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Learning.objects.filter(Q(learningnumber__icontains=fromdate)|Q (register__user__first_name=fromdate), city__rto__user=request.user)
    return render(request, "rto_search_ll.html", locals())

def rto_search_dl(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Driving.objects.filter(Q(drivingnumber__icontains=fromdate)|Q (register__user__first_name=fromdate), city__rto__user=request.user)
    return render(request, "rto_search_dl.html", locals())

def admin_search_ll(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Learning.objects.filter(Q(learningnumber__icontains=fromdate)|Q (register__user__first_name=fromdate))
    return render(request, "admin_search_ll.html", locals())

def admin_search_dl(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        data2 = True
        data = Driving.objects.filter(Q(drivingnumber__icontains=fromdate)|Q (register__user__first_name=fromdate))
    return render(request, "admin_search_dl.html", locals())

@login_required(login_url='/admin_login/')
def reg_user(request):
    data = Registration.objects.all()
    d = {'data': data}
    return render(request, "reg_user.html", d)

@login_required(login_url='/admin_login/')
def driving_licence(request, pid):
    register = Registration.objects.get(id=pid)
    data = Driving.objects.filter(register__id=pid)
    return render(request, "driving_licence.html", locals())

@login_required(login_url='/admin_login/')
def learning_licence(request, pid):
    register = Registration.objects.get(id=pid)
    data = Learning.objects.filter(register__id=pid)
    return render(request, "learning_licence.html", locals())

@login_required(login_url='/admin_login/')
def about(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        About.objects.filter(id=1).update(pagetitle=pagetitle, description=description)
        messages.success(request, "Update About Successful")
        return redirect('about')
    data = About.objects.get(id=1)
    return render(request, "about.html", locals())

@login_required(login_url='/admin_login/')
def contact(request):
    if request.method == "POST":
        pagetitle = request.POST['pagetitle']
        description = request.POST['description']
        email = request.POST['email']
        mobile = request.POST['mobile']
        timing = request.POST['timing']

        Contact.objects.filter(id=1).update(timing=timing, pagetitle=pagetitle, description=description, email=email)
        messages.success(request, "Update Contact Successful")
        return redirect('contact')
    data = Contact.objects.get(id=1)
    return render(request, "contact.html", locals())

@login_required(login_url='/admin_login/')
def admin_user_ll(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        city = request.POST['city']

        data = Learning.objects.filter(creationdate__date__gte=fromdate, creationdate__date__lte=todate, city__id=city)
        data2 = True
    city = City.objects.all()
    return render(request, "admin_user_ll.html", locals())

@login_required(login_url='/admin_login/')
def admin_user_dl(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']
        city = request.POST['city']

        data = Driving.objects.filter(creationdate__date__gte=fromdate, creationdate__date__lte=todate, city__id=city)
        data2 = True
    city = City.objects.all()
    return render(request, "admin_user_dl.html", locals())

def add_contact(request):
    if request.method == "POST":
        contact = ContactForm(request.POST, request.FILES, instance=None)
        if contact.is_valid():
            new_contact = contact.save()
            new_contact.save()
        messages.success(request, "add_contact Successful")
        return redirect('mail')
    return render(request, "mail.html", locals())

@login_required(login_url='/admin_login/')
def edit_contact(request, pid):
    Contact2.objects.filter(id=pid).update(status="read")
    data = Contact2.objects.get(id=pid)
    d = {'data': data}
    return render(request, "edit_contact.html", locals())

@login_required(login_url='/admin_login/')
def contactlist(request):
    action = request.GET.get('action')
    if action == 'read':
        data = Contact2.objects.filter(status='read')
    else:
        data = Contact2.objects.filter(status='unread')
    d = {'data': data}
    return render(request, "view_contact.html", d)

@login_required(login_url='/admin_login/')
def delete_contact(request, pid):
    data = Contact2.objects.get(id=pid)
    data.delete()
    messages.success(request, "Delete Successful")
    return redirect('contactlist')

@login_required(login_url='/rto_login/')
def rto_user_ll(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Learning.objects.filter(creationdate__date__gte=fromdate, creationdate__date__lte=todate, city__rto__user=request.user)
        data2 = True
    return render(request, "rto_user_ll.html", locals())

@login_required(login_url='/rto_login/')
def rto_user_dl(request):
    data = None
    data2 = None
    if request.method == "POST":
        fromdate = request.POST['fromdate']
        todate = request.POST['todate']

        data = Driving.objects.filter(creationdate__date__gte=fromdate, creationdate__date__lte=todate, city__rto__user=request.user)
        data2 = True
    return render(request, "rto_user_dl.html", locals())
