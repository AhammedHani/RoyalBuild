from django.http import HttpResponse
from django.shortcuts import redirect, render
from MyApp.models import *
from django.core.files.storage import FileSystemStorage

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
    return render(request,'signin.html')

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
    return render(request,'Admin/admin_home.html')

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
    data = complaint.objects.all()
    return render(request,'Admin/view_complaint.html', {'data': data})

def view_review(request):
    data = review.objects.all()
    return render(request,'Admin/view_review.html', {'data': data})

# Scheduler

def scheduler_home(request):
    return render(request,'Scheduler/scheduler_home.html')

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




# Public

def public_home(request):
    return render(request,'Public/public_home.html')