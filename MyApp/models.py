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
    CUSTOMER = models.ForeignKey(customer, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "complaint"
        
class review(models.Model):
    review_id = models.IntegerField(primary_key=True)
    review_message = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    CUSTOMER = models.ForeignKey(customer, on_delete=models.CASCADE,default=1)
    class Meta:
        db_table = "review"
        
