from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from NurtureHealthApp.models import Department, Contact_Us, register_table, add_treatment,cart, Order,Reviews,Appointments,Feedback
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from NurtureHealthApp.forms import add_treatment_form
from django.db.models import Q
from django.core.mail import EmailMessage
# Create your views here

def index(request):
    recent = ContactUs.objects.all().order_by("-id")[:5]
    deps = Department.objects.all().order_by("Dep_name")

    return render(request,"Homes.html",{"messages":recent,"department":deps})

def HomeP(request):
    return render(request,"Homes.html")


# def BkAppt(request):
#     return render(request,"BookAppointment.html")    

def ContactUS(request):
    all_data = Contact_Us.objects.all().order_by("-id")
    if request.method=="POST":
        nm = request.POST["name"]
        em = request.POST.get('emailid',False)
        con = request.POST["contact"]
        addr = request.POST["address"]
        sub = request.POST["subject"]
        msz = request.POST["message"]

        data = Contact_Us(name=nm,emailid=em,contact_number=con,address=addr,subject=sub,message=msz)
        data.save()
        res = "Dear {} Thanks for your feedback".format(nm)
        return render(request,"ContactUs.html",{"status":res,"messages":all_data})
        # return HttpResponse("<h1 style='color:green'>Dear {} Data saved Successfully</h1>".format(nme))

    return render(request,"ContactUs.html",{"messages":all_data})
 

def Departments(request):
    deps = Department.objects.all()
    return render(request,"Department.html",{"department":deps})   

def HeadFoot(request):
    return render(request,"HeadFoot.html")

def Review(request):
    return render(request,"Reviews.html")

def AboutUS(request):
    return render(request,"AboutUs.html")  

def doctors(request):
    context = {}
    department_id = request.POST.get("id")
    depart = Department.objects.order_by("name")
    context["departments"] = depart 

    #doctors = User.objects.filter(is_staff=True,is_superuser=False).order_by("first_names")

    doctors = register_table.objects.filter(occupation=department_id)
    context["doctors"] = doctors
    context["len"] = len(doctors)
    department_name = Department.objects.filter(id=department_id).first()
    context["department_name"] = department_name
    return render(request, 'doctors.html', context)

def about(request):
    context = {}
    doctors = register_table.objects.filter(user__is_staff=True,user__is_superuser=False)
    context["doctors"] = doctors

    total_doctors = doctors.count()
    context["total_doctors"] = total_doctors
    
    total_patients = register_table.objects.filter(user__is_staff=False,user__is_superuser=False).count()
    context["total_patients"] = total_patients

    total_departments = Department.objects.all().count()
    context["total_departments"] = total_departments
    context["active_about"] = "active"
    return render(request, 'About.html', context) 

def doctor_profile(request):
    context = {}
    doctor_id = request.GET["id"]
    doctor = get_object_or_404(register_table,user__id=doctor_id)
    context["doctor"] = doctor
    reviews = Reviews.objects.filter(doctor=doctor_id)
    context["reviews"] = reviews
    patient = register_table.objects.filter(user__is_superuser=False,user__is_staff=False)
    context["patients"] = patient
    if request.method == 'POST':
        doctor = User.objects.get(id=doctor_id)
        patient = User.objects.get(id=request.user.id)
        # department = Department.objects.get(id = register_table.objects.get(user__id = doctor_id).specialization.id)
        contact = request.POST["contact"]
        date = request.POST["date"]
        time = request.POST["time"]
        disease = request.POST["disease"]
        message = request.POST["message"]
        apoint = Appointments(patient=patient,doctor=doctor,contact=contact,date=date,time=time,disease=disease,message=message,status="pending")
        apoint.save()
        context["status"] = "Your appointment request to Dr. {} {} send successfully!".format(doctor.first_name,doctor.last_name)
    context["active_dash"] = "active"
    return render(request,'doctorprofile.html', context)


@login_required
def profile_reviews(request):
    context = {}
    check = register_table.objects.filter(user__id=request.user.id).first
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        reviews = Reviews.objects.filter(doctor=request.user.id)
        context["reviews"] = reviews
        patients = register_table.objects.filter(user__is_superuser=False,user__is_staff=False)
        context["patients"] = patients
    context["active_dash"] = "active"
    context["reviews_active"] = "active"
    return render(request, "profile_reviews.html", context)    

def all_doctors(request):
    context = {}
    depart = Department.objects.order_by("name")
    context["departments"] = depart 

    doctors = SignUp.objects.order_by("user__first_name")
    context["doctors"] = doctors
    context["len"] = len(doctors)
    context["department_name"] = "Doctors"

    if "q_name" in request.GET or "q_city" in request.GET:
        q_name = request.GET["q_name"]
        q_city = request.GET["q_city"]
        #doctors = SignupTable.objects.filter(user__first_name__contains=q_name)
        doctors = SignUp.objects.filter(Q(user__first_name__contains=q_name)&Q(clinic_address__contains=q_city))
        context["doctors"] = doctors
        context["len"] = len(doctors)
    return render(request, 'all_doctors.html', context)    




def SignUp(request):
    if request.method=="POST":
        fname = request.POST["first"]
        last = request.POST["last"]
        un = request.POST["uname"]
        pwd = request.POST["password"]
        em = request.POST["email"]
        con = request.POST["contact"]
        tp = request.POST["utype"]
        
        usr = User.objects.create_user(un,em,pwd)
        usr.first_name = fname
        usr.last_name = last
        if tp=="doc":
            usr.is_staff = True
        usr.save()

        reg = register_table(user=usr, contact_number=con)
        reg.save()
        return render(request,"Homes.html",{"status":"Mr/Miss. {} your Account created Successfully".format(fname)})
    return render(request,"SignUpForm.html")

def check_user(request):
    if request.method=="GET":
        un = request.GET["usern"]
        check = User.objects.filter(username=un)
        if len(check) == 1:
            return HttpResponse("Exists")
        else:
            return HttpResponse("Not Exists")

def ForgPassword(request):
    return render(request,"ForgPassword.html") 

def login_page(request):
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["password"]

        user = authenticate(username=un,password=pwd)
        if user:
            login(request,user)
            if user.is_superuser:
                return HttpResponseRedirect("/admin")
            else:
                return HttpResponseRedirect("/patient_dashboard")
            # if user.is_active:
            #     return HttpResponseRedirect("/patient_dashboard")
            
        else:
            return render(request,"ContactUs.html",{"status":"Invalid Username or Password"})


    return HttpResponse("Called")

@login_required
def patient_dashboard(request):
    context={}
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"patient_dashboard.html",context)


@login_required
def doctor_dashboard(request):
    context={}
    check=register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    return render(request,"doctor_dashboard.html",context)


@login_required
def profile_mypatients(request):
    context = {}
    check = data = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        appointments = Appointments.objects.filter(doctor=request.user.id,status="Confirmed")
        context["appointments"] = appointments
        patients = register_table.objects.filter(user__is_superuser=False,user__is_staff=False)
        context["patients"] = patients
    context["active_dash"] = "active"
    context["mypatient_active"] = "active"
    return render(request, 'patient_dashboard.html', context)    

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

# def edit_profile(request):
#     context = {}
#     check = register_table.objects.filter(user__id=request.user.id)
#     if len(check)>0:
#         data = register_table.objects.get(user__id=request.user.id)
#         context["data"]=data
#     if request.method=="POST":
#         fn=request.POST["fname"]
#         ln=request.POST["lname"]
#         em = request.POST["email"]
#         con = request.POST["contact"]
#         age = request.POST["age"]
#         ct = request.POST["city"]
#         gen = request.POST["gender"]
#         occ = request.POST["occ"]
#         abt = request.POST["about"]
#         # scpl = request.POST.get('scplz',False)

#         usr = User.objects.get(id=request.user.id)
#         usr.first_name = fn
#         usr.last_name = ln
#         usr.email = em
#         usr.save()

#         data.contact_number = con
#         data.age = age
#         data.city = ct
#         data.gender = gen
#         data.occupation = occ
#         data.about = abt
#         data.save()

#         if "image" in request.FILES:
#             img = request.FILES["image"]
#             data.profile_pic = img
#             data.save()

#         # d = Department.objects.filter(id=scpl)
#         # data.specialization = d
#         # data.save()    

#         context["status"] = "Changes Saved Successfully!!!"
#     return render(request,"edit_profile.html",context)

@login_required
def edit_profile(request):
    context = {}
    check = data = register_table.objects.filter(user__id=request.user.id)
    if len(check)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        

    if request.method == "POST":
        fname = request.POST["first_name"]
        lname = request.POST["last_name"]
        email = request.POST["email"]
        contact = request.POST["contact_number"]
        age = request.POST["age"]
        qualification = request.POST["qualification"]
        gender = request.POST["gender"]
        address_one = request.POST["address_one"]
        address_two = request.POST["address_two"]
        city = request.POST["city"]
        state = request.POST["state"]
        country = request.POST["country"]
        postal_code = request.POST["postal_code"]
        about = request.POST["about"]
        clinic_info = request.POST["clinic_info"]
        clinic_address = request.POST["clinic_address"]
        # specialization = request.POST["specialization"]
        fee = request.POST["fee"]

        usr = User.objects.get(id=request.user.id)
        usr.first_name = fname
        usr.last_name = lname
        usr.email = email
        usr.save()

        data.contact_number = contact
        data.age = age
        data.gender = gender
        data.qualification = qualification
        data.address_one = address_one
        data.address_two = address_two
        data.city = city
        data.state = state
        data.country = country
        data.postal_code = postal_code
        data.about = about
        data.clinic_info = clinic_info
        data.clinic_address = clinic_address
        data.fee = fee
        data.save()

        if "profile_pic" in request.FILES:
            try:
                os.remove(settings.MEDIA_ROOT+"/"+str(data.profile_pic))
            except:
                pass
            profile_pic = request.FILES.get("profile_pic")
            data.profile_pic = profile_pic
            data.save()
        
        # d = Departments.objects.get(id=specialization)
        # data.specialization = d
        # data.save()

        context["status"] = "Changes Saved Successfully!"
    
    context["active_dash"] = "active"
    context["settings_active"] = "active"
    return render(request, 'edit_profile.html', context)
    
    
def change_password(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    if request.method=="POST":
        current = request.POST["cpwd"]
        new_pas = request.POST["npwd"]
        
        user = User.objects.get(id=request.user.id)
        un = user.username
        check = user.check_password(current)
        if check==True:
            user.set_password(new_pas)
            user.save()
            context["msz"] = "Password Changed Successfully!!!"
            context["col"] = "alert-success"
            user = User.objects.get(username=un)
            login(request,user)
        else:
            context["msz"] = "Incorrect Current Password"
            context["col"] = "alert-danger"

    return render(request,"change_password.html",context)

def add_treatment_view(request):
    context={}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    form = add_treatment_form()
    if request.method=="POST":
        form = add_treatment_form(request.POST,request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            login_user = User.objects.get(username=request.user.username)
            data.doctor = login_user 
            data.save()
            context["status"] = "{} Added Successfully!!".format(data.treatment_name)

    context["form"] = form

    return render(request,"addtreatment.html",context)

def my_treatments(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
    all = add_treatment.objects.filter(doctor__id=request.user.id).order_by("-id")
    context["treatments"] = all
    return render(request,"mytreatments.html",context)

def single_treatment(request):
    context = {}
    id = request.GET["tid"]
    obj = add_treatment.objects.get(id=id)
    context["treatment"] = obj
    return render(request,"single_treatment.html",context)

def update_treatment(request):
    context = {}
    deps = Department.objects.all().order_by("Dep_name")
    context["department"] = deps
    tid = request.GET["tid"]
    treatment = get_object_or_404(add_treatment,id=tid)
    context["treatment"] = treatment

    if request.method=="POST":
        tn = request.POST["tname"]
        ct_id = request.POST["tcat"]
        op = request.POST["top"]
        ap = request.POST["tap"]
        des = request.POST["des"]

        cat_obj = Department.objects.get(id=ct_id) 

        treatment.treatment_name = tn
        treatment.treatment_category = cat_obj
        treatment.treatment_originalprice = op
        treatment.treatment_actualprice = ap
        treatment.details = des
        if "timg" in request.FILES:
            img = request.FILES["timg"]
            treatment.treatment_image = img
        treatment.save()
        context["status"] = "Changes saved Succesfully!!"
        context["id"] = tid

    return render(request,"update_treatment.html",context)

def delete_treatment(request):
    context = {}
    if "tid" in request.GET:
        tid = request.GET["tid"]
        trd = get_object_or_404(add_treatment,id=tid)
        context["treatment"] =trd

        if "action" in request.GET:
            trd.delete()
            context["status"] = str(trd.treatment_name)+"Deleted Successfully!!"

    return render(request,"deleteproduct.html",context)


def all_treatments(request):
    context = {}
    all_treatments = add_treatment.objects.all().order_by("treatment_name")
    context["treatments"] = all_treatments 
    if "qry" in request.GET:
        q = request.GET["qry"]
        # p = request.GET["price"]
        # trd = add_treatment.objects.filter(treatment_name__contains=q)
        trd = add_treatment.objects.filter(Q(treatment_name__icontains=q)|Q(treatment_category__Dep_name__icontains=q))
        # trd = add_treatment.objects.filter(Q(treatment_name__icontains=q)& Q(treatment_actualprice__lt=p))
        context["treatments"] = trd
        context["abc"] = "search"
    if "dep" in request.GET:
        did = request.GET["dep"]
        trd = add_treatment.objects.filter(treatment_category__id=did)
        context["treatments"] = trd
        context["abc"] = "search"

    return render(request,"alltreatments.html",context)

def sendemail(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data
        
        if request.method=="POST":
            rec = request.POST["to"].split(",")
            print(rec)
            sub = request.POST["sub"]
            msz = request.POST["msz"]

            try:
                em = EmailMessage(sub,msz,to=rec)
                em.send()
                context["status"] = "Email sent"
                context["cls"] = "alert-success"
            except:
                context["status"] = "Could not Send,Please check Internet Connection / Email Address"
                context["cls"] = "alert-danger"
                

    return render(request,"sendemail.html",context)

def forgotpass(request):
    context = {}
    if request.method=="POST":
        un = request.POST["username"]
        pwd = request.POST["npass"]

        user = get_object_or_404(User,username=un)
        user.set_password(pwd)
        user.save()
        login(request,user)
        if user.is_superuser:
            return HttpResponse("/admin")
        else:
            return HttpResponseRedirect("/patient_dashboard")

        # context["status"] = "Password Changed Successfully!!"


    return render(request,"forgot_pass.html",context)

import random

def reset_password(request):
    un = request.GET["username"]
    try:
        user = get_object_or_404(User,username=un)
        otp = random.randint(1000,9999)
        msz = "Dear {} \n{} is your One Time Password (OTP) \nDo not share it with others \nThanks&Regards \n NurtureHealth".format(user.username, otp)
        try:
            email = EmailMessage("Account Verification",msz,to=[user.email])
            email.send()
            return JsonResponse({"status":"sent","email":user.email,"rotp":otp})
        except:
            return JsonResponse({"status":"error","email":user.email})

        
    except:
        return JsonResponse({"status":"failed"})

def add_to_cart(request):
    context = {}
    items = cart.objects.filter(user__id=request.user.id,status=False)
    context["items"] = items
    if request.user.is_authenticated:
       if request.method=="POST":
            tid = request.POST["tid"]
            qty = request.POST["qty"]
            is_exist = cart.objects.filter(treatment__id=tid,user__id=request.user.id,status=False)
            if len(is_exist)>0:
                context["msz"] = "Item Already Exists in your Cart"
                context["cls"] = "alert alert-warning"
            else:
                treatment = get_object_or_404(add_treatment,id=tid)
                usr = get_object_or_404(User,id=request.user.id)
                c = cart(user=usr,treatment=treatment,quantity=qty)
                c.save()
                context["msz"] = "{} Added in Your Cart".format(treatment.treatment_name)
                context["cls"] = "alert alert-success"
                print(items)
       
    else:
        context["status"] = "Please Login First to view cart"

    return render(request,"cart.html",context)

def get_chart_data(request):
    items = cart.objects.filter(user__id=request.user.id, status=False)
    actualprice,total,quantity = 0,0,0
    for i in items:
        print()
        actualprice += float(i.treatment.treatment_actualprice)*i.quantity
        total += float(i.treatment.treatment_originalprice)*i.quantity
        quantity += int(i.quantity)

    res = {
        "total":total,"offer":actualprice,"quan":quantity
    }

    return JsonResponse(res)

def change_quan(request):
    if "quantity" in request.GET:
        cid = request.GET["cid"]
        qty = request.GET["quantity"]
        cart_obj = get_object_or_404(cart,id=cid)
        cart_obj.quantity = qty
        cart_obj.save()
        return HttpResponse(cart_obj.quantity)

    if "delete_cart" in request.GET:
        id = request.GET["delete_cart"]
        cart_obj = get_object_or_404(cart,id=id)
        cart_obj.delete()
        return HttpResponse(1) 

from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings

def process_payment(request):
    items = cart.objects.filter(user_id__id=request.user.id,status=False)
    treatments=""
    t_ids = ""
    amt=0
    inv = "INV-"
    cart_ids = ""
   

    for j in items:
        treatments += str(j.treatment.treatment_name)+"\n"
        t_ids += str(j.treatment.id)+","
        amt += float(j.treatment.treatment_actualprice)
        inv += str(j.id)
        cart_ids += str(j.id)+","


    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(amt),
        'item_name': treatments,
        'invoice': inv,
        'notify_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format("127.0.0.1:8000",
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format("127.0.0.1:8000",
                                              reverse('payment_cancelled')),
    }
    usr = User.objects.get(username=request.user.username)
    ord = Order(pat_id=usr,cart_id=cart_ids,treatment_ids=t_ids)
    ord.save()
    ord.invoice_id = str(ord.id)+inv
    ord.save()
    request.session["order_id"] = ord.id
 
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'process_payment.html', {'form': form})

def payment_done(request):
    if "order_id" in request.session:
        order_id = request.session["order_id"]
        ord_obj = get_object_or_404(Order,id=order_id)
        ord_obj.status=True
        ord_obj.save()
        

        for i in ord_obj.cart_id.split(",")[:-1]:
            cart_object = cart.objects.get(id=i)
            cart_object.status=True
            cart_object.save()
    return render(request,"payment_success.html")

def payment_cancelled(request):
    return render(request,"payment_failed.html")


def treatment_history(request):
    context = {}
    ch = register_table.objects.filter(user__id=request.user.id)
    if len(ch)>0:
        data = register_table.objects.get(user__id=request.user.id)
        context["data"] = data

    all_orders= []   
    orders = Order.objects.filter(pat_id__id=request.user.id).order_by("-id")
    for order in orders:
        treatments = []
        for id in order.treatment_ids.split(",")[:-1]:
            treat = get_object_or_404(add_treatment, id=id)
            treatments.append(treat)
        ord = {
            "order_id":order.id,
            "treatments":treatments,
            "invoice":order.invoice_id,
            "status":order.status,
            "date":order.processed_on,
        }
        all_orders.append(ord)
    context["treatment_history"] = all_orders
    return render(request,"treatment_history.html",context)

def Reviewpage(request):
    data = Feedback.objects.all().order_by("-id")
    print(data)
    if request.method=="POST":
        nm = request.POST["name"]
        cpic = request.POST["cover_pic"]
        des = request.POST["description"]
        add = request.POST["added_on"]
        data = Review(name=nm,cover_pic=cpic,description=des,added_on=add)
        data.save()
        context={"Reviewpage":data}
    return render(request,"ReviewPage.html",{"Reviewpage":data})


