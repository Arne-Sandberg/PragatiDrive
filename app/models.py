# models contain the class diagram of the database
# The models are mapped automatically to 
# database(mentioned in the shareCloud/settings.py eg. sqlite, mysql, postgresql, etc) tables
 
# Necessary imports
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
  
def upload_file(instance, filename):
    custompath='documents/' + str(instance.user.id) +'/'+ str(instance.upfile.name)
    return custompath # Return the end filename where you want it saved.


# model to store the details about the tenant e.g. Nirma, IET, etc
class Tenant(models.Model):
	name = models.CharField(max_length=60)
	#all space in Bytes
	space = models.CharField(max_length=6)
	def __unicode__(self):
		return self.name

# model to store the details about the user type e.g. Previliged, Standard, Tenant Admin
class User_Type(models.Model):
	uTypeId = models.AutoField(primary_key=True)
	tenant = models.ForeignKey(Tenant)
	userType = models.CharField(max_length=1)
	maxStorage = models.CharField(max_length=6)
	allowedExt = models.CharField(max_length=150)
	#Size in Bytes
	maxSize = models.CharField(max_length=6)
	def __unicode__(self):
		return self.userType

# model to store extra details about the user apart from the one mentioned in default User model
class User_More(models.Model):
	user = models.OneToOneField(User)
	tenant = models.ForeignKey(Tenant)
	userType = models.ForeignKey(User_Type)
	def __unicode__(self):
		return self.user.username

# model to store the details about the uploaded file by a given user
class File(models.Model):
	user = models.ForeignKey(User)
	tenant = models.ForeignKey(Tenant)	
	dateTime = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now=True)
	upfile = models.FileField(upload_to=upload_file)
	#user defined delete() method. Overides the inbult delete()
	def delete(self, *args, **kwargs):
		os.remove(os.path.join(settings.MEDIA_ROOT, self.upfile.name))
		super(File, self).delete(*args,**kwargs)
	


