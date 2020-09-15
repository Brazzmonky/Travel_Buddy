from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from django.utils import timezone
import datetime



class UserManager(models.Manager):
	def register_validator(self, postData):
		errors= {}
		validusername=User.objects.filter(username=postData['username'])
		if len(validusername) > 0:
			errors['username']="Username already in use. Please log in or choose another"
		if len(postData['username']) < 3:
			errors['username']="Required field, please choose a Username of at least 3 characters"
		if len(postData ['user_name']) < 3:
			errors['user_name'] = "Required field, please input a name of at least 3 letters"
		if len(postData ['password']) < 8:
			errors['password']= "Required field, please input a password of at least 8 characters"
		if postData['password']	!= postData['confirmpw']:
			errors['confirmpw']= "Passwords must match"
		return errors


	def login_validator(self,postData):
		validusername=User.objects.filter(username=postData['username'])
		errors= {}
		if len(postData['username']) == 0:
			errors['username']= "Required field please enter a valid Username."
		if len(validusername) < 1:
			errors['username']="No matching Username found, please register or try another Username."
		else:
			user=User.objects.get(username=postData['username'])	
			if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				print("password match")
			else:
				errors['passwordfailed']= "Incorrect password, please try again."
				print("failed password")
		return errors



class User(models.Model):
	user_name=models.CharField(max_length=255)
	username=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	objects = UserManager()
	def __repr__(self):
		return f'User: {self.user_name} {self.username} ({created_at}) ({updated_at})'

class TripManager(models.Manager):
	def trip_validator(self,postData):
		errors = {}
		if postData['start'] < str(datetime.date.today()):
			errors['start']="Trips cannot start in the past unless you have a Tardis."
		if str(postData['start']) > str(postData['end']):
			errors['end']="you're not Dr.Who, please pick an end date after the start date"	
		if len(postData['trip_name']) == 0:
			errors['trip_name']="Required field please enter a destination."
		if len(postData['description']) == 0:
			errors['description']="Required field please enter a description."
		
		return errors			


class Trip(models.Model):
	trip_name=models.CharField(max_length=255)
	description=models.CharField(max_length=255)
	start=models.DateTimeField()
	end=models.DateTimeField()
	created_at=models.DateTimeField(auto_now_add=True)
	updated_at=models.DateTimeField(auto_now_add=True)
	user=models.ManyToManyField(User, related_name="trip")
	objects = TripManager()
	def __repr__(self):
		return f'Trip: {self.trip_name} {self.description} ({self.start}) ({self.end}) ({self.created_at}) ({self.updated_at})'