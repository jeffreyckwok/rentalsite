# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login_app.models import User
from django.db import models

# Create your models here.
class CarManager(models.Manager):
    def addCar(self, carInfo):
        new_car = Car.objects.create(vehiclename=carInfo['vname'],passengers=carInfo['pass'],transmission=carInfo['trans'],description=carInfo['desc'],photo_id=carInfo['photo'],rentalprice=carInfo['price'])

class Car(models.Model):
    vehiclename = models.CharField(max_length=255)
    passengers = models.IntegerField()
    transmission = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    rentalprice = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CarManager()
    def __str__(self):
        return self.vehiclename

class PhotoManager(models.Manager):
    def addPhoto(self, photoInfo):
        new_photo = Photo.objects.create(picture=photoInfo['pic'])

class Photo(models.Model):
    car_id = models.ForeignKey(Car, related_name="car_photos")
    picture = models.ImageField(upload_to = 'img/', default = '/img/no-img.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PhotoManager()
    def __str__(self):
        return self.picture.url

class ReservationManager(models.Manager):
    def addReservation(self, resInfo):
        new_res = Reservation.objects.create(startdate=resInfo['startdate'],enddate=resInfo['enddate'],starttime=resInfo['starttime'],endtime=resInfo['endtime'],comments=resInfo['comments'],user_id=resInfo['user_id'],vehicle_id=resInfo['vehicle_id'])

class Reservation(models.Model):
    startdate = models.DateField(null=True)
    enddate = models.DateField(null=True)
    starttime = models.TimeField(null=True)
    endtime = models.TimeField(null=True)
    comments = models.TextField(max_length=1000)
    user_id = models.ForeignKey(User, related_name='users')
    vehicle_id = models.ForeignKey(Car, related_name='cars')
    charge_id = models.CharField(max_length=234)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReservationManager()
    def __str__(self):
        return str(self.vehicle_id) + " " + str(self.startdate) + " to " + str(self.enddate)
