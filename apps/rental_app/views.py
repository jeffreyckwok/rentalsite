# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, Car, Photo, Reservation
from datetime import datetime, timedelta
from rentalsite import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def addCar(request):
    carInfo = {
        vname: request.POST['vehiclename'],
        numpass: request.POST['passengers'],
        trans: request.POST['transmission'],
        desc: request.POST['description'],
        rprice: request.POST['rentalprice'],
    }

def index(request):
    return render(request, 'rental_app/index.html')

# def admin(request):
#     return render(request, 'rental_app/admin.html')

def rentals(request):
        all_cars = Car.objects.all().order_by('id')
        # car = Car.objects.all()
        # car_photo = car.car_photos.all()
        # all_photos = Photo.objects.filter(car_id=all_cars).order_by('car_id')[:1]
        context = {
        'all_cars': all_cars,
        # 'all_photos': car_photo
        }
        return render(request, 'rental_app/rentals.html', context)

def addtocart(request):
    request.session['vehicle_id'] = request.POST['carid']
    request.session['rentalprice'] = request.POST['dailyrate']
    request.session['startdate'] = request.POST['startdate']
    request.session['enddate'] = request.POST['enddate']
    request.session['starttime'] = request.POST['starttime']
    request.session['endtime'] = request.POST['endtime']
    request.session['comments'] = request.POST['comments']
    return redirect('/cart')

def cart(request):
    if 'vehicle_id' not in request.session:
        return render(request, 'rental_app/cart.html')
    else:
        id = request.session['vehicle_id']
        this_car = Car.objects.get(id=id)
        photo = Photo.objects.filter(car_id=this_car)
        d1 = datetime.strptime(request.session['startdate'], "%m/%d/%Y")
        d2 = datetime.strptime(request.session['enddate'], "%m/%d/%Y")
        dt = abs((d2 - d1).days)
        total = dt * int(request.session['rentalprice'])
        stripetotal = total *100
        carInfo = {
        'car': this_car,
        'photos': photo,
        'total' : total,
        'stripetotal' : stripetotal,
        'stripe_key' : settings.STRIPE_PUBLIC_KEY
        }
        return render(request, 'rental_app/cart.html', carInfo)

def info(request, id):
    this_car = Car.objects.get(id=id)
    photo = Photo.objects.filter(car_id=this_car)
    reservations = Reservation.objects.filter(vehicle_id=this_car)
    booked_dates = []
    for res in reservations:
        d1 = res.startdate
        d2 = res.enddate
        dt = d2 - d1
        for i in range(dt.days+1):
            d = d1 + timedelta(days=i)
            date_string = d.strftime('%m/%d/%Y')
            print "added day"
            print date_string
            booked_dates.append(date_string)
    carInfo = {
    'car': this_car,
    'photos': photo,
    'booked_dates': booked_dates
    }
    return render(request, 'rental_app/info.html', carInfo)

def checkout(request):
    if request.method == "POST":
        token = request.POST.get("stripeToken")

    try:
        charge = stripe.Charge.create(
            amount = request.POST['amount'],
            currency = "usd",
            source = token,
            description = request.POST['description']
        )
        request.session['charge_id'] = charge.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        return redirect('/addreservation')

def addreservation(request):
    this_user = User.objects.get(id=request.session['user_id'])
    this_car = Car.objects.get(id=request.session['vehicle_id'])
    sd = datetime.strptime(request.session['startdate'], "%m/%d/%Y")
    startdate = sd.strftime('%Y-%m-%d')
    ed = datetime.strptime(request.session['enddate'], "%m/%d/%Y")
    enddate = ed.strftime('%Y-%m-%d')
    context = {
    'user_id': this_user,
    'vehicle_id': this_car,
    'startdate': startdate,
    'enddate': enddate,
    'starttime': request.session['starttime'],
    'endtime': request.session['endtime'],
    'comments': request.session['comments'],
    'charge_id' : request.session['charge_id']
    }
    Reservation.objects.addReservation(context)

    del request.session['vehicle_id']
    del request.session['rentalprice']
    del request.session['startdate']
    del request.session['enddate']
    del request.session['starttime']
    del request.session['endtime']
    del request.session['comments']

    return redirect('/thankyou')

def thankyou(request):
    return render(request, 'rental_app/thankyou.html')
