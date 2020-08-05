from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Department(models.Model):
    Dep_name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%Y/%m/%d")    
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Dep_name

class Contact_Us(models.Model):
    name = models.CharField(max_length=250)
    emailid = models.EmailField(max_length=250,default="")
    contact_number = models.IntegerField(blank=True,unique=True)
    address = models.TextField(blank=True,null=True)
    subject = models.CharField(max_length=250)
    message = models.TextField()
    added_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Contact Us"   

class register_table(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    contact_number = models.IntegerField()
    profile_pic =models.ImageField(upload_to = "profiles/%Y/%m/%d",null=True,blank=True)
    specialization = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True,default="")
    address_one = models.CharField(max_length=100,null=True,blank=True)
    address_two = models.CharField(max_length=100,null=True,blank=True)
    age = models.CharField(max_length=250,null=True,blank=True)
    city = models.CharField(max_length=250,null=True,blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    country = models.CharField(max_length=250, null=True, blank=True)
    postal_code = models.CharField(max_length=250, null=True, blank=True)
    about = models.TextField(blank=True,null=True)
    gender = models.CharField(max_length=250,default="Male")
    occupation = models.CharField(max_length=250,null=True,blank=True)
    age = models.CharField(max_length=100,null=True,blank=True)
    clinic_info = models.CharField(max_length=250,null=True,blank=True)
    clinic_address = models.CharField(max_length=250,null=True,blank=True)
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)
    fee = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.user.username 

         

class add_treatment(models.Model):
    doctor = models.ForeignKey(User,on_delete=models.CASCADE)
    treatment_name = models.CharField(max_length=250)
    treatment_category = models.ForeignKey(Department,on_delete = models.CASCADE)
    treatment_originalprice = models.FloatField()
    treatment_actualprice = models.CharField(max_length=250)
    treatment_image = models.ImageField(upload_to="products/%Y/%m/%d")
    details = models.TextField()  

    def __str__(self):
        return self.treatment_category.Dep_name

    class Meta:
        verbose_name_plural = "Add Treatment"

class Appointments(models.Model):
    patient = models.ForeignKey(User, limit_choices_to={'is_staff': False},on_delete=models.CASCADE,related_name='appointment_patient',null=True) 
    doctor = models.ForeignKey(User, limit_choices_to={'is_superuser': False,'is_staff':True},on_delete=models.CASCADE,related_name='appointment_doctor',null=True)
    department_id = models.ForeignKey(Department,on_delete=models.CASCADE,null=True,blank=True)
    contact = models.IntegerField()
    date = models.DateField()
    time = models.TimeField()
    disease = models.CharField(max_length=250,null=True,blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now=True) 
    class Meta:
        verbose_name_plural = "Appointments"  

class Reviews(models.Model):
    patient = models.ForeignKey(User, limit_choices_to={'is_staff': False},on_delete=models.CASCADE,related_name='review_patient') 
    doctor = models.ForeignKey(User, limit_choices_to={'is_superuser': False,'is_staff':True},on_delete=models.CASCADE,related_name='review_doctor')
    appointment = models.ForeignKey(Appointments,on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=100)
    comment = models.TextField()
    added_on = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name_plural = "Reviews"  

class cart(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    treatment = models.ForeignKey(add_treatment,on_delete = models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default="False")
    added_on =models.DateTimeField(auto_now_add=True,null=True)
    update_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    pat_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=250)
    treatment_ids = models.CharField(max_length=250)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pat_id.username

class Feedback(models.Model):
    name = models.CharField(max_length=250)
    cover_pic = models.FileField(upload_to="media/%y/%m/%d")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return self.name         








        
