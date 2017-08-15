# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Car
from .models import Photo
from .models import Reservation

admin.site.register(Car)
admin.site.register(Photo)
admin.site.register(Reservation)
admin.site.site_header = 'Star Car Rentals Admin Page'

# Register your models here.
