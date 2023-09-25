from django.db import models

# Create your models here.
class Users(models.Model):
    phone_number = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True)
    points = models.IntegerField(default='0')
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.phone_number
    
class Appoinments(models.Model):
    user_id = models.ForeignKey(Users, 
                                on_delete=models.CASCADE, 
                                db_constraint=False)
    pick_up_date = models.DateField(max_length=255)
    pick_up_time = models.TimeField(max_length=255)
    pick_up_address = models.CharField(max_length=255)
    date_created = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=255, null=True)
    weight = models.IntegerField()
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user_id
    
class Bins(models.Model):
    bin_name = models.CharField(max_length=255)
    bin_type = models.CharField(max_length=255)
    bin_capacity = models.CharField(max_length=255)
    bin_location = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    associated  = models.BooleanField(default=0)
    
    def __str__(self):
        return self.bin_name
    
class Available_Slots(models.Model):
    Date = models.DateField(max_length=255)
    available_timeslots = models.TimeField(max_length=255)
    Availabilty = models.BooleanField(default=0)
    
    def __str__(self):
        return self.Date
    
class Reedemed_Vouchers(models.Model):
    user_id = models.ForeignKey(Users, 
                                on_delete=models.CASCADE, 
                                db_constraint=False)
    Type = models.CharField(max_length=255)
    Discount = models.IntegerField()
    Code = models.CharField(max_length=255)
    Usability = models.BooleanField(default=0)
    exp_date = models.DateField(max_length=255)
    
    def __str__(self):
        return self.Code
    
class Available_Vouchers(models.Model):
    Type = models.CharField(max_length=255)
    Cost = models.IntegerField()
    Discount = models.IntegerField()
    
    def __str__(self):
        return self.Code