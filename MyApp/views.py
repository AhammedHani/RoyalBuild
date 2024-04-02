from django.http import HttpResponse
from django.shortcuts import redirect, render
from MyApp.models import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime

# Create your views here.

# Signup

def signup(request):
    return render(request,'Public/signup.html')
    
def signup_post(request):
    data=customer()
    data.customer_name=request.POST.get('name')
    data.address=request.POST.get('address')
    data.pin=request.POST.get('pin')
    data.email=request.POST.get('email')
    data.phone=request.POST.get('phone')
    data.password=request.POST.get('password')
    Photo = request.FILES['photo']
    fs = FileSystemStorage()
    filename = fs.save(Photo.name, Photo) 
    uploaded_file_url = fs.url(filename)
    data.photo=uploaded_file_url
    data.save()
    data2=login()
    data2.username=request.POST.get('email')
    data2.password=request.POST.get('password')
    data2.type="customer"
    data2.save()
    return HttpResponse('''<Script>alert("Registered");window.location="/signup/";</Script>''')

# Login

def signin(request):
    return render(request,'Public/signin.html')

def signin_post(request):
    if request.method=='POST':
        username=request.POST.get('email')
        password=request.POST.get('password')
        data=login.objects.all()
        flag=0

        for i in data:
            if username==i.username and password==i.password:
                type=i.type
                flag=1
                if type=="admin":
                    request.session['admins']=username
                    return redirect("/admin_home")
                elif type=="scheduler":
                    request.session['schedulers']=username
                    return redirect("/scheduler_home")
                elif type=="customer":
                    request.session['customers']=username
                    return redirect("/customer_home")
                elif type=="staff":
                    request.session['staffs']=username
                    return redirect("/staff_home")
                else:
                    return HttpResponse('''<Script>alert("Invalid type");window.location="/signin/";</Script>''')
        if flag==0:
            return HttpResponse('''<Script>alert("Invalid user");window.location="/signin/";</Script>''')
        
# Admin

def admin_home(request):
    admin_id = request.session.get('admins')
    data = login.objects.get(username=admin_id)
    return render(request,'Admin/dashboard.html',{'data':data})

# def admin_dashboard(request):
#     return render(request,'Admin/dashboard.html')

def add_category(request):
    return render(request,'Admin/add_category.html')

def add_category_post(request):
    data=category()
    data.category_name=request.POST.get('textfield')
    data.description=request.POST.get('description')
    Photo = request.FILES['photo']
    fs = FileSystemStorage()
    filename = fs.save(Photo.name, Photo) 
    uploaded_file_url = fs.url(filename)
    data.photo=uploaded_file_url
    data.save()
    return HttpResponse('''<Script>alert("ADDED");window.location="/add_category/";</Script>''')

def view_category(request):
    categories = category.objects.all()
    return render(request, 'Admin/view_category.html', {'data': categories})

def edit_category(request,id):
    data=category.objects.get(category_id=id)
    return render(request,'Admin/edit_category.html',{'data':data})

def edit_category_post(request):
    id=request.POST['id']
    
    if 'photo' in request.FILES:
        
        cat=category.objects.get(category_id=id)
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        cat.photo=uploaded_file_url
        cat.category_name=request.POST.get('textfield')
        cat.description=request.POST.get('description')
        cat.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/view_category/"</script> ''')

    else:
        cat=category.objects.get(category_id=id)
        cat.category_name=request.POST.get('textfield')
        cat.description=request.POST.get('description')
        cat.save()
        
    return HttpResponse('''<Script>alert("EDITED");window.location="/view_category/";</Script>''')

def delete_category(request,id):
    category.objects.filter(category_id=id).delete()
    return HttpResponse('''<Script>alert("DELETED");window.location="/view_category/";</Script>''')

def add_product(request):
    data = category.objects.all()
    return render(request, 'Admin/add_product.html', {'data': data})

def add_product_post(request):
    data=product()
    data.product_name=request.POST.get('product_name')
    Photo = request.FILES['product_photo']
    data.detail1=request.POST.get('detail_1')
    data.detail2=request.POST.get('detail_2')
    data.detail3=request.POST.get('detail_3')
    data.detail4=request.POST.get('detail_4')
    data.detail5=request.POST.get('detail_5')
    data.detail6=request.POST.get('detail_6')
    data.description=request.POST.get('product_description')
    data.price=request.POST.get('product_price')
    data.quantity=request.POST.get('product_quantity')
    
    category_name = request.POST.get('category_type')
    
    data.CATEGORY_id = category_name
    
    fs = FileSystemStorage()
    filename = fs.save(Photo.name, Photo) 
    uploaded_file_url = fs.url(filename)
    data.photo=uploaded_file_url
    data.save()
    return HttpResponse('''<Script>alert("ADDED");window.location="/add_product/";</Script>''')

def view_product(request):
    data = product.objects.all()
    return render(request, 'Admin/view_product.html', {'data': data})

def edit_product(request, id):
    data = product.objects.get(product_id=id)
    data2 = category.objects.all()
    return render(request, 'Admin/edit_product.html', {'data': data, 'data2': data2})


def edit_product_post(request):
    id=request.POST['id']
    
    if 'photo' in request.FILES:
        
        var1=product.objects.get(product_id=id)
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        var1.photo=uploaded_file_url
        var1.product_name=request.POST.get('product_name')
        var1.detail1=request.POST.get('detail_1')
        var1.detail2=request.POST.get('detail_2')
        var1.detail3=request.POST.get('detail_3')
        var1.detail4=request.POST.get('detail_4')
        var1.detail5=request.POST.get('detail_5')
        var1.detail6=request.POST.get('detail_6')
        var1.description=request.POST.get('product_description')
        var1.price=request.POST.get('product_price')
        var1.quantity=request.POST.get('product_quantity')
        
        category_name = request.POST.get('category_type')
        var1.CATEGORY_id = category_name
        
        var1.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/view_product/"</script> ''')

    else:
        var1=product.objects.get(product_id=id)
        var1.product_name=request.POST.get('product_name')
        var1.detail1=request.POST.get('detail_1')
        var1.detail2=request.POST.get('detail_2')
        var1.detail3=request.POST.get('detail_3')
        var1.detail4=request.POST.get('detail_4')
        var1.detail5=request.POST.get('detail_5')
        var1.detail6=request.POST.get('detail_6')
        var1.description=request.POST.get('product_description')
        var1.price=request.POST.get('product_price')
        var1.quantity=request.POST.get('product_quantity')
        
        category_name = request.POST.get('category_type')
        var1.CATEGORY_id = category_name
        
        var1.save()
        
    return HttpResponse('''<Script>alert("EDITED");window.location="/view_product/";</Script>''')

def delete_product(request,id):
    product.objects.filter(product_id=id).delete()
    return HttpResponse('''<Script>alert("DELETED");window.location="/view_product/";</Script>''')

def add_staff(request):
    return render(request,'Admin/add_staff.html')

def add_staff_post(request):
    data=staff()
    data.staff_name=request.POST.get('staff_name')
    data.place=request.POST.get('staff_place')
    data.email=request.POST.get('staff_email')
    data.phone=request.POST.get('staff_phone')
    data.state=request.POST.get('staff_state')
    Photo = request.FILES['staff_photo']
    fs = FileSystemStorage()
    filename = fs.save(Photo.name, Photo) 
    uploaded_file_url = fs.url(filename)
    data.photo=uploaded_file_url
    data.status = "active"
    data.save()
    data1=login()
    data1.username=request.POST.get('staff_email')
    data1.password=request.POST.get('staff_phone')
    data1.type="staff"
    data1.save()
    
    return HttpResponse('''<Script>alert("ADDED");window.location="/add_staff/";</Script>''')
    
def view_staff(request):
    data = staff.objects.exclude(status="scheduler")
    return render(request, 'Admin/view_staff.html', {'data': data})

def edit_staff(request,id):
    data=staff.objects.get(staff_id=id)
    return render(request,'Admin/edit_staff.html',{'data':data})

def edit_staff_post(request):
    id=request.POST['id']
    
    if 'photo' in request.FILES:
        
        var1=staff.objects.get(staff_id=id)
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        var1.photo=uploaded_file_url
        var1.staff_name=request.POST.get('staff_name')
        var1.place=request.POST.get('staff_place')
        var1.email=request.POST.get('staff_email')
        var1.phone=request.POST.get('staff_phone')
        var1.state=request.POST.get('staff_state')
        
        var1.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/view_staff/"</script> ''')
    
    else:
        var1=staff.objects.get(staff_id=id)
        var1.staff_name=request.POST.get('staff_name')
        var1.place=request.POST.get('staff_place')
        var1.email=request.POST.get('staff_email')
        var1.phone=request.POST.get('staff_phone')
        var1.state=request.POST.get('staff_state')
        
        var1.save()
        
    return HttpResponse('''<Script>alert("EDITED");window.location="/view_staff/";</Script>''')

def delete_staff(request,id):
    staff.objects.filter(staff_id=id).delete()
    return HttpResponse('''<Script>alert("DELETED");window.location="/view_staff/";</Script>''')

def add_scheduler(request,id):
    data=staff.objects.get(staff_id=id)
    data.status = 'scheduler'
    data.save()
    data2=login()
    data2.username=data.email
    data2.password=data.phone
    data2.type="scheduler"
    data2.save()
    return HttpResponse('''<Script>alert("ALLOTED AS SCHEDULER");window.location="/view_staff/";</Script>''')

def view_scheduler(request):
    data=staff.objects.filter(status='scheduler')
    return render(request,"Admin/view_scheduler.html",{'data':data})

def edit_scheduler(request,id):
    data=staff.objects.get(staff_id=id)
    return render(request,'Admin/edit_scheduler.html',{'data':data})

def edit_scheduler_post(request):
    id=request.POST['id']
    
    if 'photo' in request.FILES:
        
        var1=staff.objects.get(staff_id=id)
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        var1.photo=uploaded_file_url
        var1.staff_name=request.POST.get('staff_name')
        var1.place=request.POST.get('staff_place')
        var1.email=request.POST.get('staff_email')
        var1.phone=request.POST.get('staff_phone')
        var1.state=request.POST.get('staff_state')
        var1.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/view_scheduler/"</script> ''')
    
    else:
        var1=staff.objects.get(staff_id=id)
        var1.staff_name=request.POST.get('staff_name')
        var1.place=request.POST.get('staff_place')
        var1.email=request.POST.get('staff_email')
        var1.phone=request.POST.get('staff_phone')
        var1.state=request.POST.get('staff_state')
        var1.save()
        
    return HttpResponse('''<Script>alert("EDITED");window.location="/view_scheduler/";</Script>''')

def delete_scheduler(request,id):
    data=staff.objects.get(staff_id=id)
    data2=login.objects.get(username=data.email)
    staff.objects.filter(staff_id=id).delete()
    data2.delete()
    return HttpResponse('''<Script>alert("DELETED");window.location="/view_scheduler/";</Script>''')


def add_vehicle(request):
    return render(request,'Admin/add_vehicle.html')

def add_vehicle_post(request):
    data=vehicle()
    data.vehicle_number=request.POST.get('vehicle_number')
    data.type=request.POST.get('vehicle_type')
    data.status='available'
    data.save()
    return HttpResponse('''<Script>alert("ADDED");window.location="/add_vehicle/";</Script>''')

def view_vehicle(request):
    data = vehicle.objects.all()
    return render(request, 'Admin/view_vehicle.html', {'data': data})

def edit_vehicle(request,id):
    data=vehicle.objects.get(vehicle_id=id)
    return render(request,'Admin/edit_vehicle.html',{'data':data})

def edit_vehicle_post(request):
    id=request.POST['id']
    var1=vehicle.objects.get(vehicle_id=id)
    var1.vehicle_number=request.POST.get('vehicle_number')
    var1.type=request.POST.get('vehicle_type')
    var1.save()
    return HttpResponse('''<script>alert("EDITED");window.location="/view_vehicle/"</script> ''')

def delete_vehicle(request,id):
    vehicle.objects.filter(vehicle_id=id).delete()
    return HttpResponse('''<Script>alert("DELETED");window.location="/view_vehicle/";</Script>''')
    
def view_complaint(request):
    data=complaint.objects.filter(status='pending')
    return render(request,'Admin/view_complaint.html', {'data': data})

def complaint_reply(request,id):
    data=complaint.objects.get(complaint_id=id)
    return render(request,'Admin/complaint_reply.html',{'data':data})

def complaint_reply_post(request,id):
    var1=complaint.objects.get(complaint_id=id)
    var1.reply=request.POST.get('complaint_reply')
    var1.status='replied'
    var1.save()
    return HttpResponse('''<script>alert("REPLIED");window.location="/view_complaint/";</script>''')

def admin_view_review(request):
    data = review.objects.all()
    return render(request,'Admin/view_review.html', {'data': data})

def admin_view_profile(request):
    admin_id = request.session.get('admins')
    data = login.objects.get(username=admin_id)
    return render(request, 'Admin/view_profile.html', {'data': data})

# def admin_change_password(request):
#     val=request.session.get('admins')
#     var=login.objects.get(username =val)
#     return render(request,"Admin/admin_change_password.html",{'data':var})

def admin_change_password_post(request):
    oldpass=request.POST['textfield']
    newpass=request.POST['textfield2']
    confirmpass=request.POST['textfield3']
    res=login.objects.filter(username=request.session['admins'],password=oldpass)
    if res.exists():
        if newpass == confirmpass:
            ress = res.update(password=newpass)
            return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location="/admin_home/"</script>''')
        else:
            return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/admin_view_profile/";</Script>''')
    else:
        return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/admin_view_profile/";</Script>''')

# Scheduler

def scheduler_home(request):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    return render(request,'Scheduler/dashboard.html',{'lg':lg})

# def scheduler_dashboard(request):
#     return render(request,'Scheduler/dashboard.html')

def view_category2(request):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data = category.objects.all()
    return render(request,'Scheduler/view_category2.html', {'lg': lg, 'data': data})

def view_product2(request,id):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    request.session['cc']=id
    data = product.objects.filter(CATEGORY_id=id)
    return render(request,'Scheduler/view_product2.html', {'lg': lg, 'data': data})

def edit_quantity(request,id):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data = product.objects.get(product_id=id)
    return render(request,'Scheduler/edit_quantity.html', {'lg': lg, 'data': data})

def edit_quantity_post(request,id):
    var1=product.objects.get(product_id=id)
    var1.quantity=request.POST.get('new_quantity')
    var1.save()
    c1=request.session['cc']
    return HttpResponse('''<script>alert("EDITED");window.location="/view_product2/'''+c1+'''"</script> ''')

def view_orders(request):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data=make_order.objects.filter(status="pending")
    return render(request,'Scheduler/view_orders.html',{'lg': lg, 'data':data})

def check_payment(request,id):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data=payment.objects.get(ORDER_id=id)
    return render(request,'Scheduler/check_payment.html',{'lg':lg, 'data':data})

def schedule_order(request,id):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data1 = make_order.objects.get(order_id=id)
    data2=vehicle.objects.filter(status="available")
    data3=staff.objects.filter(status="active")
    return render(request, 'Scheduler/schedule_order.html', {'lg':lg, 'data1': data1,'data2':data2,'data3':data3,})
 
def schedule_order_post(request,id):
    data1=make_order.objects.get(order_id=id)
    d1=product.objects.get(product_id=data1.PRODUCT_id)
    qty=int(d1.quantity)
    if qty==0:
        data1.status="out of stock"
        data1.save()
        return HttpResponse('''<script>alert("STOCK NOT AVALIABLE");window.location="/view_orders/";</script>''')
    else:   
        data1.status="confirmed"
        data1.save()
        q1=data1.quantity
        data2=product.objects.get(product_id=data1.PRODUCT_id)
        q2=data2.quantity
        result=int(q2)-int(q1)
        data2.quantity=result
        data2.save()
        
        staff_id = request.POST.get('staff')
        vehicle_id = request.POST.get('vehicle')
        selected_staff = staff.objects.get(staff_id=staff_id)
        selected_vehicle = vehicle.objects.get(vehicle_id=vehicle_id)
        
        data4 = vehicle_allot()
        data4.date = request.POST.get('deliveryDate')
        data4.time = request.POST.get('deliveryTime')
        data4.ORDER = data1
        data4.STAFF = selected_staff 
        data4.VEHICLE = selected_vehicle  
        data4.save()
        data5=staff.objects.get(staff_id=staff_id)
        data5.status="inactive"
        data5.save()
        data5=vehicle.objects.get(vehicle_id=vehicle_id)
        data5.status="unavailable"
        data5.save()
        
        return HttpResponse('''<Script>alert("SCHEDULED");window.location="/view_orders/";</Script>''')

def reject_order(request, id):
    data = make_order.objects.get(order_id=id)
    # qty=data.quantity
    # pro=make_order.objects.get(PRODUCT_id=data.PRODUCT_id)
    # pro.quantity+=qty
    # pro.save()
    if data.payment_method=='BANK':
        data.status="refunded"
    else:        
        data.status = "rejected"
    data.save()
    return HttpResponse('''<Script>
                            if (confirm("Are you sure you want to reject this order?")) {
                                alert("REJECTED");
                                window.location="/view_orders/";
                            } else {
                                window.location="/check_payment/'''+id+'''";
                            }
                          </Script>''')

def scheduler_view_profile(request):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    return render(request, 'Scheduler/view_profile.html', {'lg': lg})

# def scheduler_edit_profile(request):
#     staff_id = request.session.get('schedulers')
#     lg = staff.objects.get(email=staff_id)
#     return render(request, 'Scheduler/edit_profile.html', {'lg': lg})

def scheduler_edit_profile_post(request):
    if 'photo' in request.FILES:
        staff_id = request.session.get('schedulers')
        data = staff.objects.get(email=staff_id)
        data.staff_name = request.POST.get('name')
        data.place = request.POST.get('place')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.state = request.POST.get('state')
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        data.photo = uploaded_file_url
        data.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/scheduler_view_profile/";</script>''')
    else:
        staff_id = request.session.get('schedulers')
        data = staff.objects.get(email=staff_id)
        data.staff_name = request.POST.get('name')
        data.place = request.POST.get('place')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.state = request.POST.get('state')
        data.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/scheduler_view_profile/";</script>''')


# def scheduler_change_password(request):
#     staff_id=request.session.get('schedulers')
#     lg = staff.objects.get(email=staff_id)
#     data=login.objects.get(username=staff_id)
#     return render(request,"Scheduler/scheduler_change_password.html",{'lg':lg,'data':data})

def scheduler_change_password_post(request):
    oldpass=request.POST['textfield']
    newpass=request.POST['textfield2']
    confirmpass=request.POST['textfield3']
    res=login.objects.filter(username=request.session['schedulers'],password=oldpass)
    if res.exists():
        if newpass == confirmpass:
            ress = res.update(password=newpass)
            return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location="/scheduler_home/"</script>''')
        else:
            return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/scheduler_view_profile/";</Script>''')
    else:
        return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/scheduler_view_profile/";</Script>''')

def add_worksite(request):
    staff_id=request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    data=product.objects.all()
    return render(request,'Scheduler/add_worksite.html',{'lg':lg,'data':data})

def add_worksite_post(request):
    data=worksite()
    data.PRODUCT_id=request.POST.get('product')
    data.worksite_location=request.POST.get('location')
    
    photo1 = request.FILES['photo1']
    fs1 = FileSystemStorage()
    filename1 = fs1.save(photo1.name, photo1) 
    uploaded_file_url1 = fs1.url(filename1)
    data.photo1=uploaded_file_url1
    
    photo2 = request.FILES['photo2']
    fs2 = FileSystemStorage()
    filename2 = fs2.save(photo2.name, photo2) 
    uploaded_file_url2 = fs2.url(filename2)
    data.photo2=uploaded_file_url2
    
    photo3 = request.FILES['photo3']
    fs3 = FileSystemStorage()
    filename3 = fs3.save(photo3.name, photo3) 
    uploaded_file_url3 = fs3.url(filename3)
    data.photo3=uploaded_file_url3
    data.remark=request.POST.get('remark')
    data.save()
    return HttpResponse('''<Script>alert("ADDED");window.location="/add_worksite/";</Script>''')

def view_worksite(request):
    staff_id=request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data = worksite.objects.all()
    return render(request, 'Scheduler/view_worksite.html', {'lg' : lg , 'data' : data })

def edit_worksite(request,id):
    staff_id=request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data=worksite.objects.get(worksite_id=id)
    data2 = product.objects.all()
    return render(request,'Scheduler/edit_worksite.html',{'lg': lg , 'data':data,'data2':data2})

def edit_worksite_post(request):
    id=request.POST['id']
    
    data=worksite.objects.get(worksite_id=id)
    
    if 'photo1' in request.FILES:
        photo1 = request.FILES['photo1']
        fs1 = FileSystemStorage()
        filename1 = fs1.save(photo1.name, photo1) 
        uploaded_file_url1 = fs1.url(filename1)
        data.photo1=uploaded_file_url1
    
    if 'photo2' in request.FILES:
        photo2 = request.FILES['photo2']
        fs2 = FileSystemStorage()
        filename2 = fs2.save(photo2.name, photo2) 
        uploaded_file_url2 = fs2.url(filename2)
        data.photo2=uploaded_file_url2
    
    if 'photo3' in request.FILES:
        photo3 = request.FILES['photo3']
        fs3 = FileSystemStorage()
        filename3 = fs3.save(photo3.name, photo3) 
        uploaded_file_url3 = fs3.url(filename3)
        data.photo3=uploaded_file_url3
    
    data.PRODUCT_id=request.POST.get('product')
    data.worksite_location=request.POST.get('location')
    data.remark=request.POST.get('remark')
    data.save()
    
    return HttpResponse('''<script>alert("EDITED");window.location="/view_worksite/"</script> ''')


def delete_worksite(request,id):
    worksite.objects.filter(worksite_id=id).delete()
    return HttpResponse('''<Script>alert("DELETED");window.location="/view_worksite/";</Script>''')

def view_staffs(request):
    staff_id=request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data = staff.objects.filter(status="active")
    return render(request,'Scheduler/view_staffs.html',{'lg':lg,'data':data})

def add_duty(request, id):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data = staff.objects.get(staff_id=id)
    return render(request, 'Scheduler/add_duty.html', {'lg': lg, 'data': data})

def add_duty_post(request):
    staff_id = request.POST.get('staff')
    staff_obj = staff.objects.get(staff_id=staff_id)
    data = duty()
    data.job = request.POST.get('job')
    data.date = request.POST.get('date')
    data.time = request.POST.get('time')
    data.workstation = request.POST.get('workstation')  
    data.status = "pending"
    data.STAFF = staff_obj
    data.save()
    data1=staff.objects.get(staff_id=request.POST.get('staff'))
    data1.status="inactive"
    data1.save()
    return HttpResponse('''<script>alert("DUTY ADDED");window.location="/view_staffs/";</script>''')
    
def view_duty(request):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data = duty.objects.filter(status="pending")
    return render(request, 'Scheduler/view_duty.html', {'lg': lg, 'data': data})

def view_delivery_staff(request):
    staff_id = request.session.get('schedulers')
    lg = staff.objects.get(email=staff_id)
    
    data=staff.objects.filter(status="inactive")
    data1=vehicle_allot.objects.filter(STAFF_id__in=[ct.staff_id for ct in data])
    return render(request, 'Scheduler/view_delivery_staff.html', {'lg': lg, 'data': data1})
    
    
    

# customer

def customer_home(request):
    return render(request,'Customer/customer_home.html')

def home(request):
    return render(request,'Customer/home.html')

def view_categories(request):
    data = category.objects.all()
    return render(request, 'Customer/view_categories.html', {'data': data})

def view_products(request,id):
    request.session['cc']=id
    data5 = product.objects.filter(CATEGORY_id=id)
    return render(request, 'Customer/view_products.html', {'data': data5})




from django.db.models import Count, Avg

def view_products2(request, id):
    request.session['cc'] = id
    data = product.objects.get(product_id=id)
    d1 = review.objects.filter(PRODUCT_id=id).order_by('-date')
    reviews = review.objects.filter(PRODUCT_id=id)
    data2 = reviews

    # Initialize star_counts as a dictionary with an entry for each star rating from 1 to 5
    star_counts = {star: {'count': 0, 'percentage': 0} for star in range(1, 6)}

    # Update the count and percentage for each star rating based on the reviews
    total_reviews = reviews.count()
    for star, count in reviews.values_list('star').annotate(count=Count('star')):
        star_counts[star] = {
            'count': count,
            'percentage': (count / total_reviews) * 100,
        }

    # Calculate the overall rating
    average_rating = reviews.aggregate(Avg('star'))['star__avg']
    overall_rating = float(average_rating) if average_rating is not None else None

    return render(request, 'Customer/view_products2.html', {'d1':d1,'data': data, 'data2': data2, 'star_counts': star_counts, 'overall_rating': overall_rating})




# def view_review(request,id):
#     data = review.objects.filter(PRODUCT_id=id)
#     return render(request, 'Customer/view_review.html', {'data': data})

def add_order(request,id):
    data = product.objects.get(product_id=id)
    return render(request, 'Customer/add_order.html',{'id':id,'data':data})

def add_order_post(request,id):
    d1=product.objects.get(product_id=id)
    qty=int(d1.quantity)
    qty1=int(request.session['qty'])
    if qty==0:
        return HttpResponse('''<script>alert("STOCK NOT AVALIABLE");window.location="/view_products/";</script>''')
    else:   
        request.session['pid']=id
        request.session['qty']=request.POST.get('quantity')
        data1=make_order()
        data1.quantity=request.session['qty']
        data1.PRODUCT_id=request.session['pid']
        data11=product.objects.get(product_id=request.session['pid'])
        data1.amount=float(request.session['qty'])*float(data11.price)
        data10=customer.objects.get(email=request.session['customers'])
        data1.CUSTOMER_id=data10.customer_id
        data1.payment_method=request.POST.get('payment_method')
        data1.status="pending"
        from datetime import datetime
        data1.date=datetime.now().strftime('%Y-%m-%d')
        data1.save()
        d1=make_order.objects.last()
        
        data2=payment()
        data2.acc_number=request.POST.get('acc_number')
        data2.ifsc_code=request.POST.get('ifsc_code')
        data2.branch=request.POST.get('branch')
        data2.amount=float(request.session['qty'])*float(data11.price)
        data2.ORDER_id=d1.order_id
        m=request.POST.get('payment_method')
        if(m=="BANK"):
            data2.status="PAID"
        else:
            data2.status="COD"    
                
        data2.date=datetime.now().strftime('%Y-%m-%d')
        data2.save()
        c2=data11.CATEGORY
        return HttpResponse('''<script>alert("ORDERED");window.location="/view_products/'''+str(c2.category_id)+'''"</script> ''')

def view_order(request):
    customer_id = request.session.get('customers')
    data2 = customer.objects.get(email=customer_id)
    data = make_order.objects.filter(CUSTOMER_id=data2.customer_id).order_by('-order_id')
    return render(request, 'Customer/view_order.html', {'data': data})

# def cancel_order(request,id):
#     data2 = customer.objects.get(email=customer_id
#     return HttpResponse('''<script>alert("CANCEL REQUEST SENT");window.location="/view_order/";</script>''')

def send_complaint(request):
    return render(request, 'Customer/send_complaint.html')

def send_complaint_post(request):
    complaint_message=request.POST['complaint_message']
    var=complaint()
    var.complaint_message=complaint_message
    var.date=datetime.now().strftime('%Y-%m-%d')
    var.status='pending'
    customer_id = request.session.get('customers')
    data = customer.objects.get(email=customer_id)
    var.CUSTOMER_id=data.customer_id
    var.save()
    return HttpResponse('''<script>alert('SUCCESSFULLY SENT');window.location="/send_complaint/"</script>''')

def view_customer_complaint(request):
    customer_id = request.session['customers']
    customer_obj = customer.objects.get(email=customer_id)
    data = complaint.objects.filter(CUSTOMER_id=customer_obj.customer_id)
    return render(request, 'Customer/view_complaint.html', {'data': data})

def view_replied_complaint(request,id):
    data = complaint.objects.get(complaint_id=id)
    return render(request, 'Customer/view_replied_complaint.html', {'data': data})
    
def customer_view_profile(request):
    customer_id = request.session.get('customers')
    data = customer.objects.get(email=customer_id)
    return render(request, 'Customer/view_profile.html', {'data': data})

def customer_edit_profile(request):
    customer_id = request.session.get('customers')
    data = customer.objects.get(email=customer_id)
    return render(request, 'Customer/edit_profile.html', {'data': data})

def customer_edit_profile_post(request):
    if 'photo' in request.FILES:
        customer_id = request.session.get('customers')
        data = customer.objects.get(email=customer_id)
        data.customer_name = request.POST.get('name')
        data.address = request.POST.get('address')
        data.pin = request.POST.get('pin')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        data.photo = uploaded_file_url
        data.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/customer_view_profile/";</script>''')
    else:
        customer_id = request.session.get('customers')
        data = customer.objects.get(email=customer_id)
        data.customer_name = request.POST.get('name')
        data.address = request.POST.get('address')
        data.pin = request.POST.get('pin')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/customer_view_profile/";</script>''')

def customer_change_password(request):
    val=request.session.get('customers')
    var=login.objects.get(username =val)
    return render(request,"Customer/change_password.html",{'data':var})

def customer_change_password_post(request):
    oldpass=request.POST['textfield']
    newpass=request.POST['textfield2']
    confirmpass=request.POST['textfield3']
    res=login.objects.filter(username=request.session['customers'],password=oldpass)
    if res.exists():
        if newpass == confirmpass:
            ress = res.update(password=newpass)
            return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location="/customer_home/"</script>''')
        else:
            return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/customer_change_password/";</Script>''')
    else:
        return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/customer_change_password/";</Script>''')

def view_worksites(request):
    data = worksite.objects.all()
    return render(request, 'Customer/view_worksites.html', {'data': data})

def add_review(request,id):
    return render(request, 'Customer/add_review.html',{'id':id})

def add_review_post(request,id):
    data = review()
    data.star = request.POST.get('review')
    data.review_message = request.POST.get('message')
    data.date = datetime.now().strftime('%Y-%m-%d')
    data.status ="active"
    data.ORDER_id = id
    data2=customer.objects.get(email=request.session['customers'])
    data.CUSTOMER_id =data2.customer_id
    data.PRODUCT_id = make_order.objects.get(order_id=id).PRODUCT_id  
    data.save()
    return HttpResponse('''<script>alert("REVIEW ADDED");window.location="/view_order/";</script>''')
    


# Public

def public_home(request):
    data = category.objects.all()
    return render(request,'Public/public_home.html',{'data':data})

def public_view_categories(request):
    data = category.objects.all()
    return render(request, 'Public/public_view_categories.html', {'data': data})

def public_view_products(request,id):
    data = product.objects.filter(CATEGORY_id=id)
    return render(request, 'Public/public_view_products.html', {'data': data})

def public_view_products2(request, id):
    request.session['cc'] = id
    data = product.objects.get(product_id=id)
    d1 = review.objects.filter(PRODUCT_id=id).order_by('-date')
    reviews = review.objects.filter(PRODUCT_id=id)
    data2 = reviews

    # Initialize star_counts as a dictionary with an entry for each star rating from 1 to 5
    star_counts = {star: {'count': 0, 'percentage': 0} for star in range(1, 6)}

    # Update the count and percentage for each star rating based on the reviews
    total_reviews = reviews.count()
    for star, count in reviews.values_list('star').annotate(count=Count('star')):
        star_counts[star] = {
            'count': count,
            'percentage': (count / total_reviews) * 100,
        }

    # Calculate the overall rating
    average_rating = reviews.aggregate(Avg('star'))['star__avg']
    overall_rating = float(average_rating) if average_rating is not None else None

    return render(request, 'Public/public_view_products2.html', {'d1':d1,'data': data, 'data2': data2, 'star_counts': star_counts, 'overall_rating': overall_rating})


# def public_view_review(request,id):
#     data = review.objects.filter(PRODUCT_id=id)
#     return render(request, 'Public/public_view_review.html', {'data': data})





#staff

def staff_home(request): 
    return render(request,'Staff/staff_home.html')

def staff_view_duty(request):
    data = staff.objects.get(email=request.session['staffs'])
    data1=duty.objects.filter(STAFF_id=data.staff_id,status="pending")
    return render(request, 'Staff/staff_view_duty.html', {'data': data1})

def finish_duty(request,id):
    data=duty.objects.get(duty_id=id)
    data.status="completed"
    data.save()
    data1=staff.objects.get(staff_id=data.STAFF_id)
    data1.status="active"
    data1.save()
    return HttpResponse('''<script>alert("DUTY COMPLETED");window.location="/staff_view_duty/";</script>''')

def view_delivery(request):
    data=request.session.get('staffs')
    data2=staff.objects.get(email=data)
    data3=vehicle_allot.objects.filter(STAFF_id=data2).exclude(status="completed")
    return render(request, 'Staff/view_delivery.html', {'data3': data3})

def confirm_delivery(request,id):
    data=vehicle_allot.objects.get(vehicle_allot_id=id)
    data.status="completed"
    data.save()
    data5=make_order.objects.get(order_id=data.ORDER_id)
    data5.status="delivered"
    data5.save()
    data1=staff.objects.get(staff_id=data.STAFF_id)
    data1.status="active"
    data1.save()
    data2=vehicle.objects.get(vehicle_id=data.VEHICLE_id)
    data2.status="available"
    data2.save()
    return HttpResponse('''<script>alert("DELIVERED");window.location="/view_delivery/";</script>''')