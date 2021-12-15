from django.shortcuts import render
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.backends import django
import django.core.mail

from .form import OrderForm
from courses.models import course
from .models import Order, Payment, orderPoduct
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def place_order(request,total=0,quantity=0):
    return

