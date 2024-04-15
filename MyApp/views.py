from django.http import HttpResponse
from django.shortcuts import redirect, render
from MyApp.models import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import calendar
import datetime
from datetime import datetime
from django.utils import timezone
from django.db.models import Sum,Max,Count
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
                elif type=="accountant":
                    request.session['accountant']=username
                    return redirect("/accountant_home")
                else:
                    return HttpResponse('''<Script>alert("Invalid type");window.location="/signin/";</Script>''')
        if flag==0:
            return HttpResponse('''<Script>alert("Invalid user");window.location="/signin/";</Script>''')
        
# Admin

def admin_logout(request):
    del request.session['admins']
    return redirect('/public_home/')

def admin_home(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        admin_id = request.session.get('admins')
        data = login.objects.get(username=admin_id)
        return render(request,'Admin/dashboard.html',{'data':data})

def add_category(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request,'Admin/add_category.html')

def add_category_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        categories = category.objects.all().order_by('-category_id')
        return render(request, 'Admin/view_category.html', {'data': categories})

def view_category_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=category.objects.filter(category_name__icontains=search).order_by('-category_id')
        return render(request,"Admin/view_category.html",{'data':var})
        
def edit_category(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=category.objects.get(category_id=id)
        return render(request,'Admin/edit_category.html',{'data':data})

def edit_category_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        category.objects.filter(category_id=id).delete()
        return HttpResponse('''<Script>alert("DELETED");window.location="/view_category/";</Script>''')

def add_product(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = category.objects.all()
        return render(request, 'Admin/add_product.html', {'data': data})

def add_product_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=product()
        category_name = request.POST.get('category_type')
        if category_name=="7":
            data.color=request.POST.get('detail_1')
            data.size=request.POST.get('detail_2')
        elif category_name=="9":  
            data.color=request.POST.get('detail_1')
            data.size=request.POST.get('detail_2')
            data.shape=request.POST.get('detail_3') 
                        
        data.product_name=request.POST.get('product_name')
        Photo = request.FILES['product_photo']
        
        data.strength=request.POST.get('detail_4')
        data.description=request.POST.get('product_description')
        data.price=request.POST.get('product_price')
        data.quantity=request.POST.get('product_quantity')
               
        data.CATEGORY_id = category_name
        
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        data.photo=uploaded_file_url
        data.save()
        return HttpResponse('''<Script>alert("ADDED");window.location="/add_product/";</Script>''')

def view_product(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = product.objects.all().order_by('-product_id')
        return render(request, 'Admin/view_product.html', {'data': data})

def view_product_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=product.objects.filter(product_name__icontains=search).order_by('-product_id')
        return render(request,"Admin/view_product.html",{'data':var})
        
def edit_product(request, id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = product.objects.get(product_id=id)
        data2 = category.objects.all()
        return render(request, 'Admin/edit_product.html', {'data': data, 'data2': data2})

def edit_product_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        id=request.POST['id']
        
        if 'photo' in request.FILES:
            
            var1=product.objects.get(product_id=id)
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(Photo.name, Photo) 
            uploaded_file_url = fs.url(filename)
            var1.photo=uploaded_file_url
            var1.product_name=request.POST.get('product_name')
            var1.color=request.POST.get('detail_1')
            var1.size=request.POST.get('detail_2')
            var1.shape=request.POST.get('detail_3')
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
            var1.color=request.POST.get('detail_1')
            var1.size=request.POST.get('detail_2')
            var1.shape=request.POST.get('detail_3')
            var1.description=request.POST.get('product_description')
            var1.price=request.POST.get('product_price')
            var1.quantity=request.POST.get('product_quantity')
            
            category_name = request.POST.get('category_type')
            var1.CATEGORY_id = category_name
            
            var1.save()
            
        return HttpResponse('''<Script>alert("EDITED");window.location="/view_product/";</Script>''')

def delete_product(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        product.objects.filter(product_id=id).delete()
        return HttpResponse('''<Script>alert("DELETED");window.location="/view_product/";</Script>''')

def add_staff(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request,'Admin/add_staff.html')

def add_staff_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=staff()
        data.staff_name=request.POST.get('staff_name')
        data.address=request.POST.get('address')
        data.pin=request.POST.get('pin')
        data.email=request.POST.get('email')
        data.phone=request.POST.get('phone')
        data.state=request.POST.get('state')
        data.post=request.POST.get('post')
        data.type=request.POST.get('staff_type')
        data.dob=request.POST.get('dob')
        data.aadhaar=request.POST.get('aadhaar')
        data.nationality=request.POST.get('nationality')
        data.qualification=request.POST.get('qualification')
        data.remark=request.POST.get('remark')
        data.salary=request.POST.get('salary')
        Photo = request.FILES['staff_photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        data.photo=uploaded_file_url
        data.status = "active"
        data.save()
        if request.POST.get('post')=="accountant":
            data1=login()
            data1.username=request.POST.get('email')
            data1.password=request.POST.get('phone')
            data1.type="accountant"
            data1.save()
        elif request.POST.get('post')=="scheduler":
            data1=login()
            data1.username=request.POST.get('email')
            data1.password=request.POST.get('phone')
            data1.type="scheduler"
            data1.save()    
        else:    
            
            data1=login()
            data1.username=request.POST.get('email')
            data1.password=request.POST.get('phone')
            data1.type="staff"
            data1.save()
        return HttpResponse('''<Script>alert("ADDED");window.location="/add_staff/";</Script>''')

def view_staff(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = staff.objects.exclude(status="scheduler").order_by('-staff_id')
        return render(request, 'Admin/view_staff.html', {'data': data})

def view_staff_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=staff.objects.filter(staff_name__icontains=search).order_by('-staff_id')
        return render(request,"Admin/view_staff.html",{'data':var})

def edit_staff(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=staff.objects.get(staff_id=id)
        return render(request,'Admin/edit_staff.html',{'data':data})

def edit_staff_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        id=request.POST['id']
        
        if 'staff_photo' in request.FILES:
            
            var1=staff.objects.get(staff_id=id)
            Photo = request.FILES['staff_photo']
            fs = FileSystemStorage()
            filename = fs.save(Photo.name, Photo) 
            uploaded_file_url = fs.url(filename)
            var1.photo=uploaded_file_url
            var1.staff_name=request.POST.get('staff_name')
            var1.address=request.POST.get('address')
            var1.pin=request.POST.get('pin')
            var1.email=request.POST.get('email')
            var1.phone=request.POST.get('phone')
            var1.state=request.POST.get('state')
            var1.post=request.POST.get('post')
            var1.type=request.POST.get('staff_type')
            var1.dob=request.POST.get('dob')
            var1.aadhaar=request.POST.get('aadhaar')
            var1.nationality=request.POST.get('nationality')
            var1.qualification=request.POST.get('qualification')
            var1.remark=request.POST.get('remark')
            var1.salary=request.POST.get('salary')
            
            var1.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/view_staff/"</script> ''')
        
        else:
            var1=staff.objects.get(staff_id=id)
            var1.staff_name=request.POST.get('staff_name')
            var1.address=request.POST.get('address')
            var1.pin=request.POST.get('pin')
            var1.email=request.POST.get('email')
            var1.phone=request.POST.get('phone')
            var1.state=request.POST.get('state')
            var1.post=request.POST.get('post')
            var1.type=request.POST.get('staff_type')
            var1.dob=request.POST.get('dob')
            var1.aadhaar=request.POST.get('aadhaar')
            var1.nationality=request.POST.get('nationality')
            var1.qualification=request.POST.get('qualification')
            var1.remark=request.POST.get('remark')
            var1.salary=request.POST.get('salary')
            var1.save()
            
        return HttpResponse('''<Script>alert("EDITED");window.location="/view_staff/";</Script>''')

def delete_staff(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        staff.objects.filter(staff_id=id).delete()
        return HttpResponse('''<Script>alert("DELETED");window.location="/view_staff/";</Script>''')

# def add_scheduler(request,id):
#     data=staff.objects.get(staff_id=id)
#     data.status = 'scheduler'
#     data.save()
#     data2=login()
#     data2.username=data.email
#     data2.password=data.phone
#     data2.type="scheduler"
#     data2.save()
#     return HttpResponse('''<Script>alert("ALLOTED AS SCHEDULER");window.location="/view_staff/";</Script>''')

# def view_scheduler(request):
#     data=staff.objects.filter(status='scheduler')
#     return render(request,"Admin/view_scheduler.html",{'data':data})
# def add_scheduler(request):
#     return render(request,'Admin/add_scheduler.html')

# def add_scheduler_post(request):
#     data=scheduler()
#     data.scheduler_name=request.POST.get('scheduler_name')
#     data.address=request.POST.get('address')
#     data.pin=request.POST.get('pin')
#     data.email=request.POST.get('email')
#     data.phone=request.POST.get('phone')
#     data.state=request.POST.get('state')
#     Photo = request.FILES['scheduler_photo']
#     fs = FileSystemStorage()
#     filename = fs.save(Photo.name, Photo) 
#     uploaded_file_url = fs.url(filename)
#     data.photo=uploaded_file_url
#     # data.status = "active"
#     data.save()
#     data1=login()
#     data1.username=request.POST.get('email')
#     data1.password=request.POST.get('phone')
#     data1.type="scheduler"
#     data1.save()
#     return HttpResponse('''<Script>alert("ADDED");window.location="/add_scheduler/";</Script>''')





# def view_scheduler(request):
#     data = scheduler.objects.all()
#     return render(request, 'Admin/view_scheduler.html', {'data': data})

# def view_scheduler_post(request):
#     search=request.POST['textfield']
#     var=scheduler.objects.filter(scheduler_name__icontains=search)
#     return render(request,"Admin/view_scheduler.html",{'data':var})

# def edit_scheduler(request,id):
#     data=scheduler.objects.get(scheduler_id=id)
#     return render(request,'Admin/edit_scheduler.html',{'data':data})

# def edit_scheduler_post(request):
#     id=request.POST['id']
    
#     if 'scheduler_photo' in request.FILES:
        
#         var1=scheduler.objects.get(scheduler_id=id)
#         Photo = request.FILES['scheduler_photo']
#         fs = FileSystemStorage()
#         filename = fs.save(Photo.name, Photo) 
#         uploaded_file_url = fs.url(filename)
#         var1.photo=uploaded_file_url
#         var1.scheduler_name=request.POST.get('scheduler_name')
#         var1.address=request.POST.get('address')
#         var1.pin=request.POST.get('pin')
#         var1.email=request.POST.get('email')
#         var1.phone=request.POST.get('phone')
#         var1.state=request.POST.get('state')
#         var1.save()
#         return HttpResponse('''<script>alert("EDITED");window.location="/view_scheduler/"</script> ''')
    
#     else:
#         var1=scheduler.objects.get(scheduler_id=id)
#         var1.scheduler_name=request.POST.get('scheduler_name')
#         var1.address=request.POST.get('address')
#         var1.pin=request.POST.get('pin')
#         var1.email=request.POST.get('email')
#         var1.phone=request.POST.get('phone')
#         var1.state=request.POST.get('state')
#         var1.save()
        
#     return HttpResponse('''<Script>alert("EDITED");window.location="/view_scheduler/";</Script>''')

# def delete_scheduler(request,id):
#     data=scheduler.objects.get(scheduler_id=id)
#     data2=login.objects.get(username=data.email)
#     scheduler.objects.filter(scheduler_id=id).delete()
#     data2.delete()
#     return HttpResponse('''<Script>alert("DELETED");window.location="/view_scheduler/";</Script>''')


def add_vehicle(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request,'Admin/add_vehicle.html')

def add_vehicle_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=vehicle()
        data.vehicle_number=request.POST.get('vehicle_number')
        data.vehicle_name=request.POST.get('vehicle_name')
        data.type=request.POST.get('vehicle_type')
        Photo = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(Photo.name, Photo) 
        uploaded_file_url = fs.url(filename)
        data.photo=uploaded_file_url
        data.status='available'
        data.save()
        return HttpResponse('''<Script>alert("ADDED");window.location="/add_vehicle/";</Script>''')

def view_vehicle(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = vehicle.objects.all().order_by('-vehicle_id')
        return render(request, 'Admin/view_vehicle.html', {'data': data})

def view_vehicle_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=vehicle.objects.filter(vehicle_name__icontains=search).order_by('-vehicle_id')
        return render(request,"Admin/view_vehicle.html",{'data':var})

def edit_vehicle(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=vehicle.objects.get(vehicle_id=id)
        return render(request,'Admin/edit_vehicle.html',{'data':data})

def edit_vehicle_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        id = request.POST['id']
        if 'photo' in request.FILES:
            var1 = vehicle.objects.get(vehicle_id=id)
            var1.vehicle_number = request.POST.get('vehicle_number')
            var1.vehicle_name = request.POST.get('vehicle_name')
            var1.type = request.POST.get('vehicle_type')
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(Photo.name, Photo) 
            uploaded_file_url = fs.url(filename)
            var1.photo = uploaded_file_url
            var1.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/view_vehicle/"</script>''')
        else:
            var1 = vehicle.objects.get(vehicle_id=id)
            var1.vehicle_number = request.POST.get('vehicle_number')
            var1.vehicle_name = request.POST.get('vehicle_name')
            var1.type = request.POST.get('vehicle_type')
            var1.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/view_vehicle/"</script>''')
    
def delete_vehicle(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        vehicle.objects.filter(vehicle_id=id).delete()
        return HttpResponse('''<Script>alert("DELETED");window.location="/view_vehicle/";</Script>''')
    
def view_complaint(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=complaint.objects.filter(status='pending')
        return render(request,'Admin/view_complaint.html', {'data': data})

def view_complaint_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        fromdate=request.POST['textfield1']
        todate=request.POST['textfield2']
        var = complaint.objects.filter(date__range=[fromdate, todate]).exclude(status='replied')
        return render(request, 'Admin/view_complaint.html', {'data': var})

def complaint_reply(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=complaint.objects.get(complaint_id=id)
        return render(request,'Admin/complaint_reply.html',{'data':data})

def complaint_reply_post(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        var1=complaint.objects.get(complaint_id=id)
        var1.reply=request.POST.get('message')
        var1.status='replied'
        var1.save()
        return HttpResponse('''<script>alert("REPLIED");window.location="/view_complaint/";</script>''')

def admin_view_review(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = review.objects.all().order_by('-review_id')
        categories = category.objects.all()
        return render(request,'Admin/view_review.html', {'data': data, 'categories': categories})

def admin_view_review_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search = request.POST.get('textfield')
        if search:
            var = review.objects.filter(PRODUCT_id__CATEGORY_id__category_name__icontains=search)
        else:
            var = review.objects.all().order_by('-review_id')
        categories = category.objects.all()
        return render(request, "Admin/view_review.html", {'data': var, 'categories': categories})

def admin_view_profile(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        admin_id = request.session.get('admins')
        data = login.objects.get(username=admin_id)
        return render(request, 'Admin/view_profile.html', {'data': data})

# def admin_change_password(request):
#     val=request.session.get('admins')
#     var=login.objects.get(username =val)
#     return render(request,"Admin/admin_change_password.html",{'data':var})

def admin_change_password_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
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

def staff_report1(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request, 'Admin/staff_report1.html')

def view_permanent_staff(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = staff.objects.filter(type="Permanent").exclude(post="scheduler").exclude(post="accountant")
        return render(request, 'Admin/view_permanent_staff.html', {'data': data})

def view_permanent_staff_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search, type="Permanent")
        else:
            var = staff.objects.filter(type="Permanent").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Admin/view_permanent_staff.html", {'data': var})

def view_temporary_staff(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = staff.objects.filter(type="Temporary").exclude(post="scheduler").exclude(post="accountant")
        return render(request, 'Admin/view_temporary_staff.html', {'data': data})

def view_temporary_staff_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search, type="Temporary")
        else:
            var = staff.objects.filter(type="Temporary").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Admin/view_temporary_staff.html", {'data': var})

# def product_report1(request):
#     data = category.objects.all()
#     return render(request, 'Admin/product_report1.html',{'data':data})

# def product_report1_post(request):
#     search=request.POST['textfield']
#     var=category.objects.filter(category_name__icontains=search)
#     return render(request,"Admin/product_report1.html",{'data':var})

# def product_report2(request,id):
#     data = product.objects.all()
#     return render(request, 'Admin/product_report2.html', {'data': data})

# def product_report2_post(request):
#     search=request.POST['textfield']
#     var=product.objects.filter(CATEGORY_id__category_name__icontains=search)
#     return render(request,"Admin/product_report2.html",{'data':var})

def admin_view_duty1(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = duty.objects.filter(STAFF_id=id).order_by('-duty_id')
        return render(request,"Admin/admin_view_duty.html",{'data':data})

def admin_view_duty2(request,id):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data = duty.objects.filter(STAFF_id=id).order_by('-duty_id')
        return render(request,"Admin/admin_view_duty.html",{'data':data})

from django.shortcuts import render
from datetime import datetime

def sales_report1(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 5, -1))
        return render(request, 'Admin/sales_report1.html', {'years': years})

def view_sales_report1(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        a1=request.POST.get('month')
        a2=request.POST.get('year')
        request.session['m']=a1
        request.session['y']=a2
        data = make_order.objects.filter(month=a1).filter(year=a2).filter(status='delivered')
        return render(request, 'Admin/view_sales_report1.html', {'data': data})

def view_sales_report1_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=make_order.objects.filter(PRODUCT__product_name__icontains=search, status='delivered',month=request.session['m'],year=request.session['y'])
        return render(request,"Admin/view_sales_report1.html",{'data':var})

def sales_report2(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 5, -1))  
        return render(request, 'Admin/sales_report2.html', {'years': years})

def view_sales_report2(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        a1=request.POST.get('month')
        a2=request.POST.get('year')
    
        ss1=make_order.objects.order_by('PRODUCT_id').values('PRODUCT_id').filter(month=a1).filter(year=a2).annotate(sum=Count('amount')).aggregate(Max('sum'))
        # print(ss1)
        q=make_order.objects.filter(month=a1).filter(year=a2).values_list('PRODUCT_id', flat=True).annotate(sum=Count('amount')).order_by('-sum').first()
        # print(q)
        data = product.objects.filter(product_id=q)
        return render(request, 'Admin/view_sales_report2.html', {'data': data,'data2':ss1})

def view_sales_report2_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=make_order.objects.filter(PRODUCT__product_name__icontains=search, status='delivered')
        return render(request,"Admin/view_sales_report2.html",{'data':var})

def staff_wages1(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request, 'Admin/staff_wages1.html')

def staff_wages1_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        data=request.POST.get('date')
        data1=wage.objects.filter(date=data).order_by('-wage_id')
        return render(request,"Admin/view_staff_wages.html",{'data1':data1})
    
def staff_wages1_post2(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=wage.objects.filter(STAFF__staff_name__icontains=search).order_by('-wage_id')
        return render(request,"Admin/view_staff_wages.html",{'data1':var})   
        
def staff_salary1(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 5, -1))  
        return render(request, 'Admin/staff_salary1.html',{'years': years})

def staff_salary1_post(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        a1=request.POST.get('month')
        a2=request.POST.get('year')
        data = salary_slip.objects.filter(month=a1).filter(year=a2).order_by('-salary_slip_id')
        return render(request, 'Admin/view_staff_salary.html' ,{'data': data})

def staff_salary1_post2(request):
    if 'admins' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=salary_slip.objects.filter(STAFF__staff_name__icontains=search).order_by('-salary_slip_id')
        return render(request,"Admin/view_staff_salary.html",{'data':var}) 




# Scheduler --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def scheduler_logout(request):
    del request.session['schedulers']
    return redirect('/public_home/')

def scheduler_home(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        return render(request,'Scheduler/dashboard.html',{'lg':lg})

def view_category2(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = category.objects.all()
        return render(request,'Scheduler/view_category2.html', {'lg': lg, 'data': data})

def view_category2_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        search=request.POST['textfield']
        var=category.objects.filter(category_name__icontains=search)
        return render(request,"Scheduler/view_category2.html",{'lg': lg,'data':var})

def view_product2(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        request.session['cc']=id
        data = product.objects.filter(CATEGORY_id=id)
        return render(request,'Scheduler/view_product2.html', {'lg': lg, 'data': data})

def view_product2_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        search=request.POST['textfield']
        category_id=request.session.get('cc')
        var=product.objects.filter(product_name__icontains=search, CATEGORY_id=category_id)
        return render(request,"Scheduler/view_product2.html",{'lg': lg,'data':var})

def edit_quantity(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = product.objects.get(product_id=id)
        return render(request,'Scheduler/edit_quantity.html', {'lg': lg, 'data': data})

def edit_quantity_post(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        var1=product.objects.get(product_id=id)
        var1.quantity=int(var1.quantity)+int(request.POST.get('new_quantity'))
        var1.save()
        c1=request.session['cc']
        return HttpResponse('''<script>alert("UPDATED");window.location="/view_product2/'''+c1+'''"</script> ''')

def view_orders(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data=make_order.objects.filter(status="pending")
        return render(request,'Scheduler/view_orders.html',{'lg': lg, 'data':data})

def check_payment(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data=payment.objects.get(ORDER_id=id)
        return render(request,'Scheduler/check_payment.html',{'lg':lg, 'data':data})

def schedule_order(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data1 = make_order.objects.get(order_id=id)
        data2=vehicle.objects.filter(status="available")
        data3=staff.objects.filter(status="active", post="driver")
        return render(request, 'Scheduler/schedule_order.html', {'lg':lg, 'data1': data1,'data2':data2,'data3':data3,})
 
def schedule_order_post(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
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

def orders_history(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data=make_order.objects.all().order_by('-order_id')
        return render(request,'Scheduler/view_orders_history.html',{'lg': lg, 'data':data})

def orders_history_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        search = request.POST.get('textfield')
        if search:
            var = make_order.objects.filter(status__icontains=search).order_by('-order_id')
        else:
            var = make_order.objects.all().order_by('-order_id')
        return render(request, "Scheduler/view_orders_history.html", {'data': var})

def scheduler_view_profile(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        return render(request, 'Scheduler/view_profile.html', {'lg': lg})

# def scheduler_edit_profile(request):
#     staff_id = request.session.get('schedulers')
#     lg = staff.objects.get(email=staff_id)
#     return render(request, 'Scheduler/edit_profile.html', {'lg': lg})

def scheduler_edit_profile_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        if 'photo' in request.FILES:
            staff_id = request.session.get('schedulers')
            data = staff.objects.get(email=staff_id)
            data.staff_name = request.POST.get('name')
            data.dob = request.POST.get('dob')
            data.address = request.POST.get('address')
            data.pin = request.POST.get('pin')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.state = request.POST.get('state')
            data.nationality = request.POST.get('nationality')
            data.qualification = request.POST.get('qualification')
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
            data.dob = request.POST.get('dob')
            data.address = request.POST.get('address')
            data.pin = request.POST.get('pin')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.state = request.POST.get('state')
            data.nationality = request.POST.get('nationality')
            data.qualification = request.POST.get('qualification')
            data.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/scheduler_view_profile/";</script>''')

# def scheduler_change_password(request):
#     staff_id=request.session.get('schedulers')
#     lg = staff.objects.get(email=staff_id)
#     data=login.objects.get(username=staff_id)
#     return render(request,"Scheduler/scheduler_change_password.html",{'lg':lg,'data':data})

def scheduler_change_password_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        data=product.objects.all()
        return render(request,'Scheduler/add_worksite.html',{'lg':lg,'data':data})

def add_worksite_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = worksite.objects.all().order_by('-worksite_id')
        return render(request, 'Scheduler/view_worksite.html', {'lg' : lg , 'data' : data })

def edit_worksite(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data=worksite.objects.get(worksite_id=id)
        data2 = product.objects.all()
        return render(request,'Scheduler/edit_worksite.html',{'lg': lg , 'data':data,'data2':data2})

def edit_worksite_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        worksite.objects.filter(worksite_id=id).delete()
        return HttpResponse('''<Script>alert("DELETED");window.location="/view_worksite/";</Script>''')

def view_staffs(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = staff.objects.filter(status="active").exclude(post="scheduler").exclude(post="accountant")
        return render(request,'Scheduler/view_staffs.html',{'lg':lg,'data':data})

def view_staffs_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search).exclude(status="inactive")
        else:
            var = staff.objects.exclude(status="inactive").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Scheduler/view_staffs.html", {'data': var})

def add_duty(request, id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = staff.objects.get(staff_id=id)
        return render(request, 'Scheduler/add_duty.html', {'lg': lg, 'data': data})

def add_duty_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
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
    
# def view_duty(request):
#     if 'schedulers' not in request.session:
#         return redirect('/public_home/')
#     else:
#         scheduler_id = request.session.get('schedulers')
#         lg = staff.objects.get(email=scheduler_id)
        
#         data = duty.objects.all()
#         return render(request, 'Scheduler/view_duty.html', {'lg': lg, 'data': data})

# def view_delivery_staff(request):
#     if 'schedulers' not in request.session:
#         return redirect('/public_home/')
#     else:
#         scheduler_id = request.session.get('schedulers')
#         lg = staff.objects.get(email=scheduler_id)
        
#         data=staff.objects.filter(status="inactive")
#         data1=vehicle_allot.objects.filter(STAFF_id__in=[ct.staff_id for ct in data])
#         return render(request, 'Scheduler/view_delivery_staff.html', {'lg': lg, 'data': data1})
    
def view_cancel_request(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = make_order.objects.filter(status="cancel requested")
        return render(request, 'Scheduler/view_cancel_request.html', {'lg': lg, 'data': data})

def view_cancel_request_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        fromdate=request.POST['textfield1']
        todate=request.POST['textfield2']
        var = make_order.objects.filter(date__range=[fromdate, todate],  status='cancel requested')
        return render(request, 'Scheduler/view_cancel_request.html', {'data': var})

def cancel_confirm(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        data2 = make_order.objects.get(order_id=id)
        data2.status="cancelled"
        data2.save()
        data7 = vehicle_allot.objects.get(ORDER_id=id)
        data7.status="cancelled"
        data7.save()
        d1=vehicle.objects.get(vehicle_id=data7.VEHICLE_id)
        d1.status="available"
        d1.save()
        d2=staff.objects.get(staff_id=data7.STAFF_id)
        d2.status="active"
        d2.save()
        q=int(data2.quantity)
        data5=product.objects.get(product_id=data2.PRODUCT_id)
        q1=int(data5.quantity)
        q2=q1+q
        data5.quantity=q2
        data5.save()
        return HttpResponse('''<script>alert("CANCELLED");window.location="/view_cancel_request/";</script>''')
    
def view_return(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = returns.objects.filter(status="pending")
        return render(request, 'Scheduler/view_return.html', {'lg': lg, 'data': data})

def view_return_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        fromdate=request.POST['textfield1']
        todate=request.POST['textfield2']
        var = returns.objects.filter(date__range=[fromdate, todate], status='pending')
        return render(request, 'Scheduler/view_return.html', {'data': var})

def schedule_return(request,id): 
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:   
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data1 = returns.objects.get(returns_id=id)
        data5=make_order.objects.get(order_id=data1.ORDER_id)
        data2=vehicle.objects.filter(status="available")
        data3=staff.objects.filter(status="active", post="driver")
        return render(request, 'Scheduler/schedule_return.html', {'lg':lg, 'data1': data1,'data2':data2,'data3':data3,'data5':data5})

def schedule_return_post(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        data1=returns.objects.get(returns_id=id)
        data1.status="confirmed"
        data1.save()
        data2=make_order.objects.get(order_id=data1.ORDER_id)
        data2.status="return confirmed"
        data2.save()
        # d1=product.objects.get(product_id=data2.PRODUCT_id)
        # qty=int(d1.quantity) 
        # qty1=int(data2.quantity)
        # qty2=qty+qty1
        # d1.quantity=qty2
        # d1.save()
        staff_id = request.POST.get('staff')
        vehicle_id = request.POST.get('vehicle')
        
            
        data4 = vehicle_allot()
        data4.date = request.POST.get('deliveryDate')
        data4.time = request.POST.get('deliveryTime')
        data4.ORDER_id = data2.order_id
        data4.STAFF_id= request.POST.get('staff')
        data4.VEHICLE_id = request.POST.get('vehicle')
        
        data4.status="return requested"
        
        data4.save()
        data5=staff.objects.get(staff_id=staff_id)
        data5.status="inactive"
        data5.save()
        data5=vehicle.objects.get(vehicle_id=vehicle_id)
        data5.status="unavailable"
        data5.save()
            
        return HttpResponse('''<Script>alert("SCHEDULED");window.location="/view_return/";</Script>''')
    
def schedule_return_cancel(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:   
        data=returns.objects.get(returns_id=id)
        data.status="return rejected"
        
        print(data.ORDER_id)
        order_id=data.ORDER_id
        data2=make_order.objects.get(order_id=order_id)
        data2.status="return rejected"
        data2.save()
        data.save()
        return HttpResponse('''<Script>alert("RETURN REQUEST CANCELLED");window.location="/view_return/";</Script>''')

def scheduler_sales_report1(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 5, -1))
        return render(request, 'Scheduler/scheduler_sales_report1.html', {'lg':lg,'years': years})

def scheduler_view_sales_report1(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        a1=request.POST.get('month')
        a2=request.POST.get('year')
        request.session['m']=a1
        request.session['y']=a2
        data = make_order.objects.filter(month=a1).filter(year=a2).filter(status='delivered')
        return render(request, 'Scheduler/scheduler_view_sales_report1.html', {'lg':lg,'data': data})

def scheduler_view_sales_report1_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        search=request.POST['textfield']
        var=make_order.objects.filter(PRODUCT__product_name__icontains=search, status='delivered',month=request.session['m'],year=request.session['y'])
        return render(request,"Scheduler/scheduler_view_sales_report1.html",{'lg':lg,'data':var})

def scheduler_sales_report2(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 5, -1))  
        return render(request, 'Scheduler/scheduler_sales_report2.html', {'lg':lg,'years': years})

def scheduler_view_sales_report2(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        a1=request.POST.get('month')
        a2=request.POST.get('year')
    
        ss1=make_order.objects.order_by('PRODUCT_id').values('PRODUCT_id').filter(month=a1).filter(year=a2).annotate(sum=Count('amount')).aggregate(Max('sum'))
        # print(ss1)
        q=make_order.objects.filter(month=a1).filter(year=a2).values_list('PRODUCT_id', flat=True).annotate(sum=Count('amount')).order_by('-sum').first()
        # print(q)
        data = product.objects.filter(product_id=q)
        return render(request, 'Scheduler/scheduler_view_sales_report2.html', {'lg':lg,'data': data,'data2':ss1})

def scheduler_view_sales_report2_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        search=request.POST['textfield']
        var=make_order.objects.filter(PRODUCT__product_name__icontains=search, status='delivered')
        return render(request,"Scheduler/scheduler_view_sales_report2.html",{'lg':lg,'data':var})

def scheduler_staff_report1(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        return render(request, 'Scheduler/scheduler_staff_report1.html',{'lg':lg})

def scheduler_view_permanent_staff(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        
        data = staff.objects.filter(type="Permanent").exclude(post="scheduler").exclude(post="accountant")
        return render(request, 'Scheduler/scheduler_view_permanent_staff.html', {'lg':lg,'data': data})

def scheduler_view_permanent_staff_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search, type="Permanent")
        else:
            var = staff.objects.filter(type="Permanent").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Scheduler/scheduler_view_permanent_staff.html", {'lg': lg, 'data': var})

def scheduler_view_temporary_staff(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)      
        data = staff.objects.filter(type="Temporary").exclude(post="scheduler").exclude(post="accountant")
        return render(request, 'Scheduler/scheduler_view_temporary_staff.html', {'lg':lg,'data': data})

def scheduler_view_temporary_staff_post(request):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search, type="Temporary")
        else:
            var = staff.objects.filter(type="Temporary").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Scheduler/scheduler_view_temporary_staff.html", {'lg': lg, 'data': var})

def scheduler_view_duty1(request,id):
    if 'schedulers' not in request.session:
        return redirect('/public_home/')
    else:
        scheduler_id = request.session.get('schedulers')
        lg = staff.objects.get(email=scheduler_id)      
        data = duty.objects.filter(STAFF_id=id).order_by('-duty_id')
        return render(request,"Scheduler/scheduler_view_duty.html",{'lg':lg,'data':data})

# def scheduler_view_duty2(request,id):
#     if 'schedulers' not in request.session:
#         return redirect('/public_home/')
#     else:
#         data = duty.objects.filter(STAFF_id=id)
#         return render(request,"Scheduler/scheduler_view_duty.html",{'data':data})
    
    
    
    
# Customer--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def customer_logout(request):
    del request.session['customers']
    return redirect('/public_home/')

def customer_home(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request,'Customer/customer_home.html')

def home(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request,'Customer/home.html')

def view_categories(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = category.objects.all()
        return render(request, 'Customer/view_categories.html', {'data': data})

def category_sub(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        request.session['category']=id
        data = category.objects.get(category_id=id)
        if data.category_name=="Bricks" or data.category_name=="Paving":
            return render(request, 'Customer/category_sub.html',{'data':data})
        else:
            data5 = product.objects.filter(CATEGORY_id=request.session['category'])
            return render(request, 'Customer/view_products.html', {'data': data5})        

def view_categories1(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        if request.session['category']=='paving':
            data5 = product.objects.filter(CATEGORY_id=request.session['category']).filter(color=request.POST.get('color')).filter(size=request.POST.get('size')).filter(shape=request.POST.get('shape'))
            return render(request, 'Customer/view_products.html', {'data': data5})
        else:
            data5 = product.objects.filter(CATEGORY_id=request.session['category']).filter(color=request.POST.get('color')).filter(size=request.POST.get('size'))
            return render(request, 'Customer/view_products.html', {'data': data5})

from django.db.models import Count, Avg

def view_products2(request, id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = product.objects.get(product_id=id)
        return render(request, 'Customer/add_order.html',{'id':id,'data':data})

def add_order_post(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        d1=product.objects.get(product_id=id)
        qty=int(d1.quantity)
        qty1=int(request.POST.get('quantity'))
        
        if qty==0:
            return HttpResponse('''<script>alert("STOCK NOT AVALIABLE");window.location="/view_categories/";</script>''')
        elif qty1>qty:
            return HttpResponse('''<script>alert("STOCK NOT AVALIABLE");window.location="/view_categories/";</script>''')
        
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
            from django.utils import timezone
            data1.date=datetime.now().strftime('%Y-%m-%d')
            data1.month=timezone.now().month
            data1.year=timezone.now().year
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
            return HttpResponse('''<script>alert("ORDERED");window.location="/view_categories/"</script> ''')

def view_order(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        customer_id = request.session.get('customers')
        data2 = customer.objects.get(email=customer_id)
        data = make_order.objects.filter(CUSTOMER_id=data2.customer_id).order_by('-order_id')
        return render(request, 'Customer/view_order.html', {'data': data})

def view_order_post(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        customer_id = request.session.get('customers')
        data2 = customer.objects.get(email=customer_id)
        search = request.POST.get('textfield')
        if search:
            var = make_order.objects.filter(CUSTOMER_id=data2.customer_id, PRODUCT_id__product_name__icontains=search).order_by('-order_id')
        else:
            var = make_order.objects.filter(CUSTOMER_id=data2.customer_id).order_by('-order_id')
        return render(request, "Customer/view_order.html", {'data': var})

def cancel_order(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data2 = make_order.objects.get(order_id=id)
        data2.status="cancel requested"
        data2.save()
        return HttpResponse('''<script>alert("CANCEL REQUEST SENT");window.location="/view_order/";</script>''')

def send_complaint(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request, 'Customer/send_complaint.html')

def send_complaint_post(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        complaint_message=request.POST['complaint_message']
        var=complaint()
        var.complaint_message=complaint_message
        var.date=datetime.now().strftime('%Y-%m-%d')
        var.status='pending'
        customer_id = request.session.get('customers')
        data = customer.objects.get(email=customer_id)
        var.CUSTOMER_id=data.customer_id
        var.save()
        return HttpResponse('''<script>alert('SUCCESSFULLY SENT');window.location="/view_customer_complaint/"</script>''')

def view_customer_complaint(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        customer_id = request.session['customers']
        customer_obj = customer.objects.get(email=customer_id)
        data = complaint.objects.filter(CUSTOMER_id=customer_obj.customer_id).order_by('-complaint_id')
        return render(request, 'Customer/view_complaint.html', {'data': data})

def view_customer_complaint_post(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        customer_id = request.session.get('customers')
        customer_obj = customer.objects.get(email=customer_id)
        fromdate=request.POST['textfield1']
        todate=request.POST['textfield2']
        var = complaint.objects.filter(CUSTOMER_id=customer_obj.customer_id, date__range=[fromdate, todate]).order_by('-complaint_id')
        return render(request, 'Customer/view_complaint.html', {'data': var})

def view_replied_complaint(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = complaint.objects.get(complaint_id=id)
        return render(request, 'Customer/view_replied_complaint.html', {'data': data})
    
def customer_view_profile(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        customer_id = request.session.get('customers')
        data = customer.objects.get(email=customer_id)
        return render(request, 'Customer/view_profile.html', {'data': data})

def customer_edit_profile(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        customer_id = request.session.get('customers')
        data = customer.objects.get(email=customer_id)
        return render(request, 'Customer/edit_profile.html', {'data': data})

def customer_edit_profile_post(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        val=request.session.get('customers')
        var=login.objects.get(username =val)
        return render(request,"Customer/change_password.html",{'data':var})

def customer_change_password_post(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
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
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = worksite.objects.all()
        return render(request, 'Customer/view_worksites.html', {'data': data})

def add_review(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        return render(request, 'Customer/add_review.html',{'id':id})

def add_review_post(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
    
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
    
def add_return(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = make_order.objects.get(order_id=id)
        return render(request, 'Customer/add_return.html', {'data': data})

def add_return_post(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = returns()
        data2 = make_order.objects.get(order_id=id)
        data2.status="return requested"
        data2.save()
        data.date = datetime.now().strftime('%Y-%m-%d')
        data.reason = request.POST.get('reason')
        data.ORDER_id=id
        data.status = "pending"
        data.save()
        #new
        # data3 = vehicle_allot.objects.get(ORDER_id=id)
        # data3.status="return requested"
        # data3.save()
        return HttpResponse('''<script>alert("RETURN REQUEST SENT");window.location="/view_order/";</script>''')

from datetime import datetime
from django.utils import timezone

def add_to_cart_post(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        quantity=request.POST.get('a')
        c=cart.objects.filter(PRODUCT_id=id).count()
        d10=product.objects.get(product_id=id)
        if c==0:
            data=cart()
            data.quantity=quantity
            data.PRODUCT_id=id
            d1=customer.objects.get(email=request.session['customers'])
            data.CUSTOMER_id=d1.customer_id
            data.date=datetime.now().strftime('%Y-%m-%d')
            data.amount=float(quantity)*float(d10.price)
            data.status="pending"
            print(timezone.now().month)
            print(timezone.now().year)
            data.month=timezone.now().month
            data.year=timezone.now().year
            data.save()
            return HttpResponse('''<script>alert("PRODUCT ADDED TO CART");window.location="/view_cart/";</script>''')
        else:
            data=cart.objects.get(PRODUCT_id=id)
            
            data.quantity=int(data.quantity)+int(quantity)
            data.amount=float(data.quantity)*float(d10.price)
            data.save()
            return HttpResponse('''<script>alert("PRODUCT ADDED TO CART");window.location="/view_cart/";</script>''')
        
def view_cart(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = customer.objects.get(email=request.session['customers'])
        data1 = cart.objects.filter(CUSTOMER_id=data.customer_id).order_by('-cart_id')
        return render(request, 'Customer/view_cart.html', {'data': data1})

def view_cart_post(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        search=request.POST['textfield']
        var=cart.objects.filter(PRODUCT_id__product_name__icontains=search).order_by('-cart_id')
        return render(request,"Customer/view_cart.html",{'data':var})

def edit_cart(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = cart.objects.get(cart_id=id)
        return render(request, 'Customer/edit_cart.html', {'data': data})

def edit_cart_post(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = cart.objects.get(cart_id=id)
        data.quantity = request.POST.get('quantity')
        data1=product.objects.get(product_id=data.PRODUCT_id)
        total=float(request.POST.get('quantity'))*float(data1.price)
        data.amount=total
        
        data.save()
        return HttpResponse('''<script>alert("EDITED");window.location="/view_cart/";</script>''')

def delete_cart(request,id):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        cart.objects.filter(cart_id=id).delete()
        return HttpResponse('''<script>alert("DELETED");window.location="/view_cart/";</script>''')

from django.db.models import Sum

def cart_orders(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = customer.objects.get(email=request.session['customers'])
        data1 = cart.objects.filter(CUSTOMER_id=data.customer_id)
        amount =cart.objects.filter(CUSTOMER_id=data.customer_id).aggregate(sum=Sum('amount'))['sum']
        return render(request, 'Customer/cart_payment.html', {'data': data1,'amount':amount})

def cart_orders1(request):
    if 'customers' not in request.session:
        return redirect('/public_home/')
    else:
        data = customer.objects.get(email=request.session['customers'])
        print(data.customer_id)
        data15 = cart.objects.filter(CUSTOMER_id=data.customer_id)
        
        
        for ct in data15:
            
            data1=make_order()
            data1.quantity=ct.quantity
            data1.PRODUCT_id=ct.PRODUCT_id
            data1.month=ct.month
            data1.year=ct.year
            data11=product.objects.get(product_id=ct.PRODUCT_id)
            data1.amount=float(ct.quantity)*float(data11.price)
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
            data2.amount=float(data1.quantity)*float(data11.price)
            data2.ORDER_id=d1.order_id
            m=request.POST.get('payment_method')
            if(m=="BANK"):
                data2.status="PAID"
            else:
                data2.status="COD"    
                    
            data2.date=datetime.now().strftime('%Y-%m-%d')
            data2.save()
        data15 = cart.objects.filter(CUSTOMER_id=data.customer_id)  
        for ct in data15:
            ct.delete()  
        c2=data11.CATEGORY
        return HttpResponse('''<script>alert("ORDERED");window.location="/view_cart/"</script> ''')

        
        return render(request, 'Customer/cart_orders.html', {'data': data1})




# Public--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def public_home(request):
    data = category.objects.all()
    return render(request,'Public/public_home.html',{'data':data})

def public_view_categories(request):
    data = category.objects.all()
    return render(request, 'Public/public_view_categories.html', {'data': data})

def public_category_sub(request,id):
    request.session['category']=id
    data = category.objects.get(category_id=id)
    if data.category_name=="Bricks" or data.category_name=="Paving":
        return render(request, 'Public/public_category_sub.html',{'data':data})
    else:
        data5 = product.objects.filter(CATEGORY_id=request.session['category'])
        return render(request, 'Public/public_view_products.html', {'data': data5})        
 
def public_view_categories1(request):
    if request.session['category']=='paving':
        data5 = product.objects.filter(CATEGORY_id=request.session['category']).filter(color=request.POST.get('color')).filter(size=request.POST.get('size')).filter(shape=request.POST.get('shape'))
        return render(request, 'Public/public_view_products.html', {'data': data5})
    else:
        data5 = product.objects.filter(CATEGORY_id=request.session['category']).filter(color=request.POST.get('color')).filter(size=request.POST.get('size'))
        return render(request, 'Public/public_view_products.html', {'data': data5})

# def public_view_products(request,id):
#     data = product.objects.filter(CATEGORY_id=id)
#     return render(request, 'Public/public_view_products.html', {'data': data})

# def public_view_products2(request, id):
#     request.session['cc'] = id
#     data = product.objects.get(product_id=id)
#     d1 = review.objects.filter(PRODUCT_id=id).order_by('-date')
#     reviews = review.objects.filter(PRODUCT_id=id)
#     data2 = reviews

#     # Initialize star_counts as a dictionary with an entry for each star rating from 1 to 5
#     star_counts = {star: {'count': 0, 'percentage': 0} for star in range(1, 6)}

#     # Update the count and percentage for each star rating based on the reviews
#     total_reviews = reviews.count()
#     for star, count in reviews.values_list('star').annotate(count=Count('star')):
#         star_counts[star] = {
#             'count': count,
#             'percentage': (count / total_reviews) * 100,
#         }

#     # Calculate the overall rating
#     average_rating = reviews.aggregate(Avg('star'))['star__avg']
#     overall_rating = float(average_rating) if average_rating is not None else None

#     return render(request, 'Public/public_view_products2.html', {'d1':d1,'data': data, 'data2': data2, 'star_counts': star_counts, 'overall_rating': overall_rating})

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

def public_view_worksites(request):
    data = worksite.objects.all()
    return render(request, 'Public/public_view_worksites.html', {'data': data})




# Staff--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def staff_logout(request):
    del request.session['staffs']
    return redirect('/public_home/')

def staff_home(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        staff_id = request.session.get('staffs')
        lg = staff.objects.get(email=staff_id)
        
        return render(request,'Staff/staff_home.html',{'lg':lg})

def staff_view_duty(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        staff_id = request.session.get('staffs')
        lg = staff.objects.get(email=staff_id)
        
        data = staff.objects.get(email=request.session['staffs'])
        data1=duty.objects.filter(STAFF_id=data.staff_id,status="pending")
        return render(request, 'Staff/staff_view_duty.html', {'lg':lg,'data': data1})

def finish_duty(request,id):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        data=duty.objects.get(duty_id=id)
        data.status="completed"
        data.save()
        data1=staff.objects.get(staff_id=data.STAFF_id)
        data1.status="active"
        data1.save()
        return HttpResponse('''<script>alert("DUTY COMPLETED");window.location="/staff_view_duty/";</script>''')

def view_delivery(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        staff_id = request.session.get('staffs')
        lg = staff.objects.get(email=staff_id)
        
        data=request.session.get('staffs')
        data2=staff.objects.get(email=data)
        data3=vehicle_allot.objects.filter(STAFF_id=data2).exclude(status="completed").exclude(status="cancelled")
        data3=data3.filter(ORDER_id__status="confirmed")
        return render(request, 'Staff/view_delivery.html', {'lg':lg,'data3': data3})

def confirm_delivery(request,id):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
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

def view_returns(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        staff_id = request.session.get('staffs')
        lg = staff.objects.get(email=staff_id)
        
        data=request.session.get('staffs')
        data2=staff.objects.get(email=data)
        data3=vehicle_allot.objects.filter(STAFF_id=data2, status="return requested")
        for i in data3:
            print(i.ORDER)
        data3=data3.filter(ORDER_id__status="return confirmed")
        
        return render(request, 'Staff/view_returns.html', {'lg':lg,'data3': data3})

def view_returns_post(request,id): 
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        data10 = vehicle_allot.objects.get(vehicle_allot_id=id)
        order_id = data10.ORDER_id
        data11 = make_order.objects.get(order_id=order_id)
        data12 = product.objects.get(product_id=data11.PRODUCT_id)
        qty=int(data12.quantity) 
        qty1=int(data11.quantity)
        qty2=qty+qty1
        data12.quantity=qty2
        data12.save()
        data13 = returns.objects.get(ORDER_id=order_id)
        data13.status="returned"
        data13.save()
        
        data=vehicle_allot.objects.get(vehicle_allot_id=id)
        data.status="return completed"
        data.save()
        data5=make_order.objects.get(order_id=data.ORDER_id)
        data5.status="returned"
        data5.save()
        data1=staff.objects.get(staff_id=data.STAFF_id)
        data1.status="active"
        data1.save()
        data2=vehicle.objects.get(vehicle_id=data.VEHICLE_id)
        data2.status="available"
        data2.save()
        
        # data1=returns.objects.get(returns_id=id)
        # data2=make_order.objects.get(order_id=data1.ORDER_id)
        # d1=product.objects.get(product_id=data2.PRODUCT_id)
        # qty=int(d1.quantity) 
        # qty1=int(data2.quantity)
        # qty2=qty+qty1
        # d1.quantity=qty2
        # d1.save()
        
        return HttpResponse('''<script>alert("DELIVERED");window.location="/view_returns/";</script>''')

def staff_view_profile(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        staff_id = request.session.get('staffs')
        lg = staff.objects.get(email=staff_id)
        return render(request, 'Staff/view_profile.html', {'lg': lg})

def staff_edit_profile_post(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        if 'photo' in request.FILES:
            staff_id = request.session.get('staffs')
            data = staff.objects.get(email=staff_id)
            data.staff_name = request.POST.get('name')
            data.dob = request.POST.get('dob')
            data.address = request.POST.get('address')
            data.pin = request.POST.get('pin')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.state = request.POST.get('state')
            data.nationality = request.POST.get('nationality')
            data.qualification = request.POST.get('qualification')
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(Photo.name, Photo) 
            uploaded_file_url = fs.url(filename)
            data.photo = uploaded_file_url
            data.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/staff_view_profile/";</script>''')
        else:
            staff_id = request.session.get('staffs')
            data = staff.objects.get(email=staff_id)
            data.staff_name = request.POST.get('name')
            data.dob = request.POST.get('dob')
            data.address = request.POST.get('address')
            data.pin = request.POST.get('pin')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.state = request.POST.get('state')
            data.nationality = request.POST.get('nationality')
            data.qualification = request.POST.get('qualification')
            data.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/staff_view_profile/";</script>''')

def staff_change_password_post(request):
    if 'staffs' not in request.session:
        return redirect('/public_home/')
    else:
        oldpass=request.POST['textfield']
        newpass=request.POST['textfield2']
        confirmpass=request.POST['textfield3']
        res=login.objects.filter(username=request.session['staffs'],password=oldpass)
        if res.exists():
            if newpass == confirmpass:
                ress = res.update(password=newpass)
                return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location="/staff_home/"</script>''')
            else:
                return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/staff_view_profile/";</Script>''')
        else:
            return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/staff_view_profile/";</Script>''')




# Accountant--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def accountant_logout(request):
    del request.session['accountant']
    return redirect('/public_home/')

def accountant_home(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        return render(request,'Accountant/accountant_home.html',{'lg':lg})

def view_wages(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        data = staff.objects.filter(type="temporary").exclude(post="accountant").exclude(post="scheduler")
        return render(request, 'Accountant/view_wages.html', {'lg':lg,'data': data})

def view_wages_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post=search, type='Temporary')
        else:
            var = staff.objects.filter(type='Temporary').exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Accountant/view_wages.html", {'lg': lg, 'data': var})

def view_salary(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        data = staff.objects.filter(type="permanent").exclude(post="accountant").exclude(post="scheduler")
        return render(request, 'Accountant/view_salary.html', {'lg':lg,'data': data})
    
def view_salary_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post=search, type='Permanent')
        else:
            var = staff.objects.filter(type='Permanent').exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Accountant/view_salary.html", {'lg': lg, 'data': var})

def add_wage(request,id):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        return render(request, 'Accountant/add_wage.html',{'lg':lg,'id':id})

def add_wage_post(request,id):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        data = wage()
        data.STAFF_id = id
        data.date=datetime.now().strftime('%Y-%m-%d')
        data.wage=request.POST.get('wage')
        data.remark = request.POST.get('remark')
        data.save()
        return HttpResponse('''<script>alert("WAGE ADDED");window.location="/view_wages/";</script>''')

def add_leave(request,id):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        return render(request, 'Accountant/add_leave.html',{'lg':lg,'id':id})

def add_leave_post(request,id):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        data=staff.objects.get(staff_id=id)
        salary=data.salary
        
        wage=float(salary)/30
        total=float(wage)*float(request.POST.get('leave'))
        nettotal=int(salary)-total
        
        l=int(request.POST.get('leave'))
        if l!=1:
            data5=salary_slip()
            data5.STAFF_id=id
            from datetime import datetime
            from django.utils import timezone
            data5.date=datetime.now().strftime('%Y-%m-%d')
            data5.month=timezone.now().month
            data5.year=timezone.now().year
            data5.leave=request.POST.get('leave')
            data5.basic_salary=data.salary
            data5.salary=nettotal
            data5.save()
            return render(request,"Accountant/view_staff_salary.html",{'lg':lg,'data':data,'netsalary':nettotal})            
        else:                           
            data5=salary_slip()
            data5.STAFF_id=id
            from datetime import datetime
            from django.utils import timezone
            data5.date=datetime.now().strftime('%Y-%m-%d')
            data5.month=timezone.now().month
            data5.year=timezone.now().year
            data5.leave=request.POST.get('leave')
            data5.basic_salary=data.salary
            data5.salary=data.salary
            data5.save()
            
            return render(request,"Accountant/view_staff_salary.html",{'lg':lg,'data':data,'netsalary':data.salary})

def accountant_view_profile(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        return render(request, 'Accountant/view_profile.html', {'lg': lg})

def accountant_edit_profile_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        if 'photo' in request.FILES:
            accountant_id = request.session.get('accountant')
            data = staff.objects.get(email=accountant_id)
            data.staff_name = request.POST.get('name')
            data.dob = request.POST.get('dob')
            data.address = request.POST.get('address')
            data.pin = request.POST.get('pin')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.state = request.POST.get('state')
            data.nationality = request.POST.get('nationality')
            data.qualification = request.POST.get('qualification')
            Photo = request.FILES['photo']
            fs = FileSystemStorage()
            filename = fs.save(Photo.name, Photo) 
            uploaded_file_url = fs.url(filename)
            data.photo = uploaded_file_url
            data.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/accountant_view_profile/";</script>''')
        else:
            accountant_id = request.session.get('accountant')
            data = staff.objects.get(email=accountant_id)
            data.staff_name = request.POST.get('name')
            data.dob = request.POST.get('dob')
            data.address = request.POST.get('address')
            data.pin = request.POST.get('pin')
            data.email = request.POST.get('email')
            data.phone = request.POST.get('phone')
            data.state = request.POST.get('state')
            data.nationality = request.POST.get('nationality')
            data.qualification = request.POST.get('qualification')
            data.save()
            return HttpResponse('''<script>alert("EDITED");window.location="/accountant_view_profile/";</script>''')

def accountant_change_password_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        oldpass=request.POST['textfield']
        newpass=request.POST['textfield2']
        confirmpass=request.POST['textfield3']
        res=login.objects.filter(username=request.session['accountant'],password=oldpass)
        if res.exists():
            if newpass == confirmpass:
                ress = res.update(password=newpass)
                return HttpResponse('''<script>alert('PASSWORD CHANGED SUCCESSFULLY');window.location="/accountant_home/"</script>''')
            else:
                return HttpResponse('''<Script>alert("PASSWORD DOES NOT MATCH");window.location="/accountant_view_profile/";</Script>''')
        else:
            return HttpResponse('''<Script>alert("CURRENT PASSWORD IS WRONG");window.location="/accountant_view_profile/";</Script>''')

def accountant_staff_report1(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        return render(request, 'Accountant/accountant_staff_report1.html',{'lg':lg})

def accountant_view_permanent_staff(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        
        data = staff.objects.filter(type="Permanent").exclude(post="scheduler").exclude(post="accountant")
        return render(request, 'Accountant/accountant_view_permanent_staff.html', {'lg':lg,'data': data})

def accountant_view_permanent_staff_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search, type="Permanent")
        else:
            var = staff.objects.filter(type="Permanent").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Accountant/accountant_view_permanent_staff.html", {'lg': lg, 'data': var})

def accountant_view_temporary_staff(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)      
        data = staff.objects.filter(type="Temporary").exclude(post="scheduler").exclude(post="accountant")
        return render(request, 'Accountant/accountant_view_temporary_staff.html', {'lg':lg,'data': data})

def accountant_view_temporary_staff_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)
        search = request.POST.get('textfield')
        if search:
            var = staff.objects.filter(post__icontains=search, type="Temporary")
        else:
            var = staff.objects.filter(type="Temporary").exclude(post="scheduler").exclude(post="accountant")
        return render(request, "Accountant/accountant_view_temporary_staff.html", {'lg': lg, 'data': var})

def accountant_view_duty1(request,id):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)      
        data = duty.objects.filter(STAFF_id=id).order_by('-duty_id')
        return render(request,"Accountant/accountant_view_duty.html",{'lg':lg,'data':data})
    
def accountant_staff_wages1(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id) 
         
        return render(request, 'Accountant/accountant_staff_wages1.html', {'lg':lg})

def accountant_staff_wages1_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)  
        
        data=request.POST.get('date')
        data1=wage.objects.filter(date=data)
        return render(request,"Accountant/accountant_view_staff_wages.html",{'lg':lg,'data1':data1})
    
def accountant_staff_wages1_post2(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)  
        
        search=request.POST['textfield']
        var=wage.objects.filter(STAFF__staff_name__icontains=search)
        return render(request,"Accountant/accountant_view_staff_wages.html",{'lg':lg,'data1':var})   
    
    
    
    
    
    
    
    
    
def accountant_staff_salary1(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)  
        
        current_year = datetime.now().year
        years = list(range(current_year, current_year - 5, -1))  
        return render(request, 'Accountant/accountant_staff_salary1.html',{'lg':lg,'years': years})

def accountant_staff_salary1_post(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)  
        
        a1=request.POST.get('month')
        a2=request.POST.get('year')
        data = salary_slip.objects.filter(month=a1).filter(year=a2).order_by('-salary_slip_id')
        return render(request, 'Accountant/accountant_view_staff_salaries.html' ,{'lg':lg,'data': data})

def accountant_staff_salary1_post2(request):
    if 'accountant' not in request.session:
        return redirect('/public_home/')
    else:
        accountant_id = request.session.get('accountant')
        lg = staff.objects.get(email=accountant_id)  
        
        search=request.POST['textfield']
        var=salary_slip.objects.filter(STAFF__staff_name__icontains=search).order_by('-salary_slip_id')
        return render(request,"Accountant/accountant_view_staff_salaries.html",{'lg':lg,'data':var}) 
    
    
    
    
    
    
    