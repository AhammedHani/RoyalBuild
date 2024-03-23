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
                else:
                    return HttpResponse('''<Script>alert("Invalid type");window.location="/signin/";</Script>''')
        if flag==0:
            return HttpResponse('''<Script>alert("Invalid user");window.location="/signin/";</Script>''')
        
# Admin

def admin_home(request):
    admin_id = request.session.get('admins')
    data = login.objects.get(username=admin_id)
    return render(request,'Admin/admin_home.html',{'data':data})

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
    return HttpResponse('''<Script>alert("Accepted");window.location="/add_category/";</Script>''')

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
        
    return HttpResponse('''<Script>alert("Edited");window.location="/view_category/";</Script>''')

def delete_category(request,id):
    category.objects.filter(category_id=id).delete()
    return HttpResponse('''<Script>alert("Deleted");window.location="/view_category/";</Script>''')

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
    return HttpResponse('''<Script>alert("Accepted");window.location="/add_product/";</Script>''')

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
        
    return HttpResponse('''<Script>alert("Edited");window.location="/view_product/";</Script>''')

def delete_product(request,id):
    product.objects.filter(product_id=id).delete()
    return HttpResponse('''<Script>alert("Deleted");window.location="/view_product/";</Script>''')

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
    
    return HttpResponse('''<Script>alert("Accepted");window.location="/add_staff/";</Script>''')
    
def view_staff(request):
    data = staff.objects.filter(status="active")
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
        
    return HttpResponse('''<Script>alert("Edited");window.location="/view_staff/";</Script>''')

def delete_staff(request,id):
    staff.objects.filter(staff_id=id).delete()
    return HttpResponse('''<Script>alert("Deleted");window.location="/view_staff/";</Script>''')

def add_scheduler(request,id):
    data=staff.objects.get(staff_id=id)
    data.status = 'scheduler'
    data.save()
    data2=login()
    data2.username=data.email
    data2.password=data.phone
    data2.type="scheduler"
    data2.save()
    return HttpResponse('''<Script>alert("Allotted as scheduler");window.location="/view_staff/";</Script>''')

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
        
    return HttpResponse('''<Script>alert("Edited");window.location="/view_scheduler/";</Script>''')

def delete_scheduler(request,id):
    data=staff.objects.get(staff_id=id)
    data2=login.objects.get(username=data.email)
    staff.objects.filter(staff_id=id).delete()
    
    
    data2.delete()
    return HttpResponse('''<Script>alert("Deleted");window.location="/view_scheduler/";</Script>''')


def add_vehicle(request):
    return render(request,'Admin/add_vehicle.html')

def add_vehicle_post(request):
    data=vehicle()
    data.vehicle_number=request.POST.get('vehicle_number')
    data.type=request.POST.get('vehicle_type')
    data.status='available'
    data.save()
    return HttpResponse('''<Script>alert("Accepted");window.location="/add_vehicle/";</Script>''')

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
    return HttpResponse('''<Script>alert("Deleted");window.location="/view_vehicle/";</Script>''')
    
def view_complaint(request):
    data=complaint.objects.filter(status='pending')
    return render(request,'Admin/view_complaint.html', {'data': data})

def view_review(request):
    data = review.objects.all()
    return render(request,'Admin/view_review.html', {'data': data})

def admin_view_profile(request):
    admin_id = request.session.get('admins')
    data = login.objects.get(username=admin_id)
    return render(request, 'Admin/view_profile.html', {'data': data})

def admin_change_password(request):
    val=request.session.get('admins')
    var=login.objects.get(username =val)
    return render(request,"Admin/admin_change_password.html",{'data':var})

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
            return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/admin_change_password/";</Script>''')
    else:
        return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/admin_change_password/";</Script>''')


# Scheduler

def scheduler_home(request):
    staff_id = request.session.get('schedulers')
    data = staff.objects.get(email=staff_id)
    return render(request,'Scheduler/scheduler_home.html',{'data':data})

def view_category2(request):
    data = category.objects.all()
    return render(request,'Scheduler/view_category2.html', {'data': data})

def view_product2(request,id):
    request.session['cc']=id
    data = product.objects.filter(CATEGORY_id=id)
    return render(request,'Scheduler/view_product2.html', {'data': data})

def edit_quantity(request,id):
    data = product.objects.get(product_id=id)
    return render(request,'Scheduler/edit_quantity.html', {'data': data})

def edit_quantity_post(request,id):
    var1=product.objects.get(product_id=id)
    var1.quantity=request.POST.get('new_quantity')
    var1.save()
    c1=request.session['cc']
    return HttpResponse('''<script>alert("EDITED");window.location="/view_product2/'''+c1+'''"</script> ''')

def view_orders(request):
    data=make_order.objects.filter(status="pending")
    return render(request,'Scheduler/view_orders.html',{'data':data})

def check_payment(request,id):
    data=payment.objects.get(ORDER_id=id)
    return render(request,'Scheduler/check_payment.html',{'data':data})

def schedule_order(request,id):
    data1 = make_order.objects.get(order_id=id)
    data2=vehicle.objects.all()
    data3=staff.objects.all()
    return render(request, 'Scheduler/schedule_order.html', {'data1': data1,'data2':data2,'data3':data3,})
 
def schedule_order_post(request,id):
    data1=make_order.objects.get(order_id=id)
    data1.status="approved"
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
    
    return HttpResponse('''<Script>alert("Scheduled");window.location="/view_orders/";</Script>''')

def reject_order(request, id):
    data = make_order.objects.get(order_id=id)
    data.status = "rejected"
    data.save()
    return HttpResponse('''<Script>alert("REJECTED");window.location="/view_order/";</Script>''')

def scheduler_view_profile(request):
    staff_id = request.session.get('schedulers')
    data = staff.objects.get(email=staff_id)
    return render(request, 'Scheduler/view_profile.html', {'data': data})

def scheduler_edit_profile(request):
    staff_id = request.session.get('schedulers')
    data = staff.objects.get(email=staff_id)
    return render(request, 'Scheduler/edit_profile.html', {'data': data})

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
        return HttpResponse('''<script>alert("Profile Edited");window.location="/scheduler_view_profile/";</script>''')
    else:
        staff_id = request.session.get('schedulers')
        data = staff.objects.get(email=staff_id)
        data.staff_name = request.POST.get('name')
        data.place = request.POST.get('place')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.state = request.POST.get('state')
        data.save()
        return HttpResponse('''<script>alert("Profile Edited");window.location="/scheduler_view_profile/";</script>''')


def scheduler_change_password(request):
    val=request.session.get('schedulers')
    var=login.objects.get(username =val)
    return render(request,"Scheduler/scheduler_change_password.html",{'data':var})

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
            return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/scheduler_change_password/";</Script>''')
    else:
        return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/scheduler_change_password/";</Script>''')



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

def view_products2(request,id):
    request.session['cc']=id
    data = product.objects.get(product_id=id)
    return render(request, 'Customer/view_products2.html', {'data': data})

def add_order(request,id):
    return render(request, 'Customer/add_order.html',{'id':id})

def add_order_post(request,id):
    request.session['pid']=id
    request.session['qty']=request.POST.get('quantity')
    return render(request,"Customer/make_payment.html")

def make_payment(request):
    data1=make_order()
    data1.quantity=request.session['qty']
    data1.PRODUCT_id=request.session['pid']
    data11=product.objects.get(product_id=request.session['pid'])
    data1.amount=int(request.session['qty'])*int(data11.price)
    data10=customer.objects.get(email=request.session['customers'])
    data1.CUSTOMER_id=data10.customer_id
    data1.status="pending"
    from datetime import datetime
    data1.date=datetime.now().strftime('%Y-%m-%d')
    data1.save()
    d1=make_order.objects.last()
    
    data2=payment()
    data2.acc_number=request.POST.get('acc_number')
    data2.ifsc_code=request.POST.get('ifsc_code')
    data2.branch=request.POST.get('branch')
    data2.amount=int(request.session['qty'])*int(data11.price)
    data2.ORDER_id=d1.order_id
    data2.status="paid"
    data2.date=datetime.now().strftime('%Y-%m-%d')
    data2.save()
    c2=data11.CATEGORY
    return HttpResponse('''<script>alert("ORDERED");window.location="/view_products/'''+str(c2.category_id)+'''"</script> ''')

def view_order(request):
    customer_id = request.session.get('customers')
    data2 = customer.objects.get(email=customer_id)
    data = make_order.objects.filter(CUSTOMER_id=data2.customer_id).order_by('-order_id')
    return render(request, 'Customer/view_order.html', {'data': data})

def send_complaint(request):
    return render(request, 'Customer/send_complaint.html')

def send_complaint_post(request):
    complaint_message=request.POST['complaint_message']
    var=complaint()
    var.complaint_message=complaint_message
    var.date=datetime.now().strftime('%Y-%m-%d')
    var.status='pending'
    var.customer_id=customer.objects.get(email=request.session['customers'])
    var.save()
    return HttpResponse('''<script>alert('Success');window.location="/send_complaint/"</script>''')
    
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
        return HttpResponse('''<script>alert("Profile Edited");window.location="/customer_view_profile/";</script>''')
    else:
        customer_id = request.session.get('customers')
        data = customer.objects.get(email=customer_id)
        data.customer_name = request.POST.get('name')
        data.address = request.POST.get('address')
        data.pin = request.POST.get('pin')
        data.email = request.POST.get('email')
        data.phone = request.POST.get('phone')
        data.save()
        return HttpResponse('''<script>alert("Profile Edited");window.location="/customer_view_profile/";</script>''')

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

# Public

def public_home(request):
    return render(request,'Public/public_home.html')