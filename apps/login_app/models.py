from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re
import datetime


EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validateReg(self, userInfo):
        errors = []
        if not userInfo['fname'].isalpha():
            errors.append('First name contains non-alpha character(s)')
        if len(userInfo['fname']) < 2:
            messages.warning(request, 'First name too short.')
        if not userInfo['lname'].isalpha():
            errors.append('Last name contains non-alpha character(s)')
        if len(userInfo['lname']) < 2:
            errors.append('Last name too short.')
        if not EMAIL_REGEX.match(userInfo['em']):
            errors.append('Email is not a valid email!')
        try:
            User.objects.get(email=userInfo['em'])
            errors.append("Email is already registered.")
        except:
            pass
        if len(userInfo['pw']) < 8:
            errors.append('Password is not long enough.')
        if userInfo['pw'] != userInfo['conf_pw']:
            errors.append('Passwords do not match.')

        if len(errors) == 0:
            userInfo['pw'] = bcrypt.hashpw(userInfo['pw'].encode('utf-8'), bcrypt.gensalt())
            new_user = User.objects.create(first_name = userInfo['fname'], last_name = userInfo['lname'], email = userInfo['em'], password = userInfo['pw'])
            return {
            'new': new_user,
            'error_list': None
            }
        else:
            return {
            'new': None,
            'error_list': errors
            }

    def userLogin(self, log_data):
        errors=[]
        try:
			found_user = User.objects.get(email=log_data['loginEmail'])
			if bcrypt.hashpw(log_data['loginPw'].encode('utf-8'), found_user.password.encode('utf-8')) != found_user.password.encode('utf-8'):
				errors.append("Incorrect password.")
        except:
			#email does not exist in the database
			errors.append("Email address not registered.")
        if len(errors)==0:
            return {
                'logged_user': found_user,
                'list_errors': None
            }
        else:
            return {
                'logged_user': None,
                'list_errors': errors
            }

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return self.email;
