from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class State(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    cityname = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cityname

class Rto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    nodalname = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=200, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Learning(models.Model):
    rto = models.ForeignKey(Rto, on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    learningnumber = models.CharField(max_length=100, null=True, blank=True)
    father = models.CharField(max_length=100, null=True, blank=True)
    birth = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    licencetype = models.CharField(max_length=100, null=True, blank=True)
    blood = models.CharField(max_length=100, null=True, blank=True)
    peraddress = models.CharField(max_length=100, null=True, blank=True)
    comaddress = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default='Not Updated Yet', null=True, blank=True)
    image2 = models.FileField(null=True, blank=True)
    aadhaar_card = models.FileField(upload_to='aadhaar_cards/', null=True, blank=True)  # ✅ NEW FIELD
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.father


class Driving(models.Model):
    register = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    rto = models.ForeignKey(Rto, on_delete=models.CASCADE, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    drivingnumber = models.CharField(max_length=100, null=True, blank=True)
    learningnumber = models.CharField(max_length=100, null=True, blank=True)
    father = models.CharField(max_length=100, null=True, blank=True)
    birth = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    licencetype = models.CharField(max_length=100, null=True, blank=True)
    blood = models.CharField(max_length=100, null=True, blank=True)
    peraddress = models.CharField(max_length=100, null=True, blank=True)
    comaddress = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default='Not Updated Yet', null=True, blank=True)
    image2 = models.FileField(null=True, blank=True)
    aadhaar_card = models.FileField(upload_to='aadhaar_cards/', null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.father

class Trackinghistory(models.Model):
    learning = models.ForeignKey(Learning, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default='Not Updated Yet', null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

class Drivinghistory(models.Model):
    driving = models.ForeignKey(Driving, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, default='Not Updated Yet', null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.remark

class About(models.Model):
    pagetitle = models.CharField(max_length=300, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.pagetitle

class Contact(models.Model):
    pagetitle = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    timing = models.CharField(max_length=100, null=True, blank=True)
    description = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.pagetitle

class Contact2(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=200, default='unread', null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
