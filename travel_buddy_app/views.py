from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt


def login_reg(request):
	return render(request, 'login.html')


def newUser(request):
	errors =User.objects.register_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/')
	else:
		password=request.POST['password']
		pw_hash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
		newUser=User.objects.create(user_name=request.POST['user_name'],username=request.POST['username'],password=pw_hash.decode())
		request.session['loggedinUserID']= newUser.id
		return redirect('/home')


def login(request):
	errors = User.objects.login_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request,value)
		return redirect('/')
	else:
		loggedinUser=User.objects.get(username=request.POST['username'])
		request.session['loggedinUserID'] = loggedinUser.id
		return redirect('/home')

def home(request):
	loggedinUser= User.objects.get(id=request.session['loggedinUserID'])
	user_trips= Trip.objects.filter(user=loggedinUser)
	other_trips= Trip.objects.exclude(user=loggedinUser)
	context={
	"loggedinUser":loggedinUser,
	"user_trips":user_trips,
	"other_trips":other_trips,

	}	
	return render(request, 'home.html', context)

def add_trip(request,userid):
	loggedinUser=User.objects.get(id=userid)
	context={
	"loggedinUser":loggedinUser,
	}
	return render(request, 'add_trip.html', context)

def Add(request,userid):
	errors=Trip.objects.trip_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect('/add_trip/' + str(userid))
	else:	
		loggedinUser=User.objects.get(id=userid)
		Newtrip=Trip.objects.create(trip_name=request.POST['trip_name'], description=request.POST['description'],start=request.POST['start'],end=request.POST['end'])
		Newtrip.user.add(loggedinUser)
		return redirect('/home')

def gohome(request):
	return redirect('/home')

def view(request,tripid):
	loggedinUser=User.objects.get(id=request.session['loggedinUserID'])
	trip_to_display=Trip.objects.get(id=tripid)
	# other_users=Trip.objects.exclude(user=creater)
	users=User.objects.filter(trip=Trip.objects.get(id=tripid))
	context={
	"trip_to_display": trip_to_display,
	# "other_users":other_users,
	"users":users,
	"loggedinUser":loggedinUser,
	}
	return render(request, 'show_destination.html', context)

def join(request,tripid):
	loggedinUser=User.objects.get(id=request.session['loggedinUserID'])
	trip_to_join=Trip.objects.get(id=tripid)
	trip_to_join.user.add(loggedinUser)
	return redirect('/home')


def logout(request):
	request.session.clear()
	return redirect('/')

