from django.db import models
             
class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    class Meta:
        db_table = "login" 
           
class category(models.Model):
    category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.FileField()
    class Meta:
        db_table = "category"
        
class product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=100)
    photo = models.FileField()
    detail1 =  models.CharField(max_length=100)
    detail2 =  models.CharField(max_length=100)
    detail3 =  models.CharField(max_length=100)
    detail4 =  models.CharField(max_length=100)
    detail5 =  models.CharField(max_length=100)
    detail6 =  models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    CATEGORY = models.ForeignKey(category, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "product"
        
class customer(models.Model):
    customer_id = models.IntegerField(primary_key=True)
    customer_name = models.CharField(max_length=100)
    photo = models.FileField()
    address = models.CharField(max_length=100)
    pin = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    class Meta:
        db_table = "customer"
        
class staff(models.Model):
    staff_id = models.IntegerField(primary_key=True)
    staff_name = models.CharField(max_length=100)
    photo = models.FileField()
    place = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    class Meta:
        db_table = "staff"

class vehicle(models.Model):
    vehicle_id = models.IntegerField(primary_key=True)
    vehicle_number = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    class Meta:
        db_table = "vehicle"
        
class complaint(models.Model):
    complaint_id = models.IntegerField(primary_key=True)
    complaint_message = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    reply = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "complaint"
        
class review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    review_message = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    star = models.IntegerField()
    status = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer, on_delete=models.CASCADE,default=1)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE,default=1)
    
    class Meta:
        db_table = "review"
        
class make_order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    status = models.CharField(max_length=100)  
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_method =  models.CharField(max_length=100)  
    CUSTOMER = models.ForeignKey(customer, on_delete=models.CASCADE,default=1)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "make_order"        

class payment(models.Model):
    payment_id = models.IntegerField(primary_key=True)
    branch = models.CharField(max_length=100)
    acc_number = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    ORDER = models.ForeignKey(make_order, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "payment" 
        
class vehicle_allot(models.Model):
    vehicle_allot_id = models.IntegerField(primary_key=True)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    ORDER = models.ForeignKey(make_order, on_delete=models.CASCADE,default=1)
    STAFF = models.ForeignKey(staff, on_delete=models.CASCADE,default=1)
    VEHICLE = models.ForeignKey(vehicle, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "vehicle_allot" 
        
class worksite(models.Model):
    worksite_id = models.IntegerField(primary_key=True)
    worksite_location = models.CharField(max_length=100)
    photo1 = models.CharField(max_length=100)
    photo2 = models.CharField(max_length=100)
    photo3 = models.CharField(max_length=100)
    remark = models.CharField(max_length=100)
    PRODUCT = models.ForeignKey(product, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "worksite" 
        
class duty(models.Model):
    duty_id = models.IntegerField(primary_key=True)
    job = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    time = models.CharField(max_length=100)
    workstation = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    STAFF = models.ForeignKey(staff, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "duty" 