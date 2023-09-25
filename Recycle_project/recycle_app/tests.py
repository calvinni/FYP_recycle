from datetime import date
import datetime
from django.test import TestCase
from .models import *
from django.contrib.auth.hashers import make_password, check_password

# Create your tests here.
class UserInsertTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(phone_number = '87654321', 
                                              password = hashedP)
        
        self.testdata = Users.objects.get(phone_number = '87654321')
    
    def tearDown(self):
        Users.objects.all().delete()    
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Users data
        self.assertEqual(self.testdata.phone_number, '87654321')
        PassCheck = check_password('TESTPASSWORD', self.testdata.password)
        self.assertEqual(PassCheck, True)
        today = date.today()
        self.assertEqual(self.testdata.date_created, today)
        self.assertEqual(self.testdata.points, 0)
        self.assertEqual(self.testdata.email, None)
        
################################################################################################

class AppoinmentsInsertTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(phone_number = '87654321', 
                                              password = hashedP)
        self.testAppointment = Appoinments.objects.create(id = -1,
                                                          user_id = self.testusers, 
                                                          pick_up_date = '2010-02-11',
                                                          pick_up_time = '18:00:00',
                                                          type = 'Metal',
                                                          weight = 10)
        
        self.testdata = Appoinments.objects.get(id = -1)
    
    def tearDown(self):
        Appoinments.objects.all().delete()  
        Users.objects.all().delete()  
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Appoinments data
        self.assertEqual(self.testdata.user_id.phone_number, '87654321')
        PassCheck = check_password('TESTPASSWORD', self.testdata.user_id.password)
        self.assertEqual(PassCheck, True)
        today = date.today()
        self.assertEqual(self.testdata.user_id.date_created, today)
        self.assertEqual(self.testdata.user_id.points, 0)
        self.assertEqual(self.testdata.user_id.email, None)
        pickupdate = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.pick_up_date, pickupdate)
        pickuptime = datetime.time(18, 0, 0)
        self.assertEqual(self.testdata.pick_up_time, pickuptime)
        self.assertEqual(self.testdata.type, 'Metal')
        self.assertEqual(self.testdata.weight, 10)
        
################################################################################################

class BinsInsertTest(TestCase):
    def setUp(self):
        self.testbins = Bins.objects.create(bin_name = 'Bin010',
                                            bin_type = 'Metal',
                                            bin_capacity = '85%',
                                            bin_location = 'test street',
                                            status = 'Online')
        
        self.testdata = Bins.objects.get(bin_name = 'Bin010')
    
    def tearDown(self):
        Bins.objects.all().delete()    
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Bins data
        self.assertEqual(self.testdata.bin_name, 'Bin010')
        self.assertEqual(self.testdata.bin_type, 'Metal')
        self.assertEqual(self.testdata.bin_capacity, '85%')
        self.assertEqual(self.testdata.bin_location, 'test street')
        self.assertEqual(self.testdata.status, 'Online')
        self.assertEqual(self.testdata.associated, 0)
        
################################################################################################

class SlotsInsertTest(TestCase):
    def setUp(self):
        self.testbins = Available_Slots.objects.create(id = -1,
                                                       Date = '2010-02-11',
                                                       available_timeslots = '18:00:00')
        
        self.testdata = Available_Slots.objects.get(id = -1)
    
    def tearDown(self):
        Available_Slots.objects.all().delete()    
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Slots data
        dateslot = datetime.date(2010, 2, 11)
        self.assertEqual(self.testdata.Date, dateslot)
        timeslot = datetime.time(18, 0, 0)
        self.assertEqual(self.testdata.available_timeslots, timeslot)
        
################################################################################################

class Reedemed_VouchersInsertTest(TestCase):
    def setUp(self):
        hashedP = make_password('TESTPASSWORD')
        self.testusers = Users.objects.create(phone_number = '87654321', 
                                              password = hashedP)
        self.testAppointment = Reedemed_Vouchers.objects.create(id = -1,
                                                                user_id = self.testusers, 
                                                                Type = 'WACDONOLD',
                                                                Discount = 15,
                                                                Code = 1523898422,
                                                                exp_date = '2010-03-11')
        
        self.testdata = Reedemed_Vouchers.objects.get(id = -1)
    
    def tearDown(self):
        Reedemed_Vouchers.objects.all().delete()  
        Users.objects.all().delete()  
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Reedemed_Vouchers data
        self.assertEqual(self.testdata.user_id.phone_number, '87654321')
        PassCheck = check_password('TESTPASSWORD', self.testdata.user_id.password)
        self.assertEqual(PassCheck, True)
        today = date.today()
        self.assertEqual(self.testdata.user_id.date_created, today)
        self.assertEqual(self.testdata.user_id.points, 0)
        self.assertEqual(self.testdata.user_id.email, None)
        self.assertEqual(self.testdata.Type, 'WACDONOLD')
        self.assertEqual(self.testdata.Discount, 15)
        self.assertEqual(self.testdata.Code, '1523898422')
        expdate = datetime.date(2010, 3, 11)
        self.assertEqual(self.testdata.exp_date, expdate)
        
################################################################################################

class Available_VouchersInsertTest(TestCase):
    def setUp(self):
        self.testbins = Available_Vouchers.objects.create(id = -1,
                                                          Type = 'WACDONOLD',
                                                          Cost = 69,
                                                          Discount = 15)
        
        self.testdata = Available_Vouchers.objects.get(id = -1)
    
    def tearDown(self):
        Available_Vouchers.objects.all().delete()    
        
    def test_usersInsert(self): #Test if data is inserted properly in users
        # Slots data
        self.assertEqual(self.testdata.Type, 'WACDONOLD')
        self.assertEqual(self.testdata.Cost, 69)
        self.assertEqual(self.testdata.Discount, 15)
        
################################################################################################