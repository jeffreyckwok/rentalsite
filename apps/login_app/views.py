# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request, 'login_app/index.html')

def register(request):
    context = {
    'fname': request.POST['first_name'],
    'lname': request.POST['last_name'],
    'pw': request.POST['password'],
    'conf_pw': request.POST['confirm_password'],
    'em': request.POST['email'],
    }
    regResults = User.objects.validateReg(context)

    if regResults['new'] != None:
        request.session['user_id'] = regResults['new'].id
        request.session['user_firstname'] = regResults['new'].first_name
        return redirect('/login/success')
    else:
        for error_str in regResults['error_list']:
            messages.add_message(request, messages.ERROR, error_str)
        return redirect('/login')

def success(request):
    if 'user_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/login')
    else:
        return render(request, 'rental_app/index.html')

def login(request):
    userLog = {
        'loginEmail': request.POST['email'],
        'loginPw': request.POST['password']
    }

    login_results = User.objects.userLogin(userLog)

    if login_results['list_errors'] != None:
        for error in login_results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/index')
    else:
        request.session['user_id'] = login_results['logged_user'].id
        request.session['user_firstname'] = login_results['logged_user'].first_name
        return redirect('/login/success')

def logout(request):
	request.session.clear()
	return redirect('/')
