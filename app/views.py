# Necessary imports
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.contrib.auth.models import User
from .models import Tenant, User_Type, User_More, File
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.cache import cache
from django.db.models import Max
import string
#import os

#cache handle
USER_FILES = "files"


# login() view authenticates the user and redirects to the right url
# If the session is already set it redirects user directly to the 
# page based on it's credentials. If the session is not redirect the request
# to authView() for authentication
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/app/loggedin')
	c={}
	c.update(csrf(request))
	return render_to_response('app/login.html',c)

# authView() authenticates the user based on the input credentials
def authView(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)

	if user is not None:
		auth.login(request,user)
		return HttpResponseRedirect('/app/loggedin')
	else:
		return HttpResponseRedirect('/app/invalid')	

# loggedin() view checks the type of the user and redirects it to
# the respective url
def loggedin(request):
	username=request.user.username
	userid=request.user.id
	#update the cache here
	cache.set(USER_FILES, _get_files(request.user))
	if userid==1:
		return HttpResponseRedirect('/app/superuser')
	
	x=User_More.objects.filter(user_id=userid)
	userTenant=x[0].tenant
	userType=x[0].userType
	if userType.userType==unicode('N'):
		return HttpResponseRedirect('/app/standard_user')	
	elif userType.userType==unicode('P'):
		return HttpResponseRedirect('/app/privileged_user')	
	elif userType.userType==unicode('A'):
		return HttpResponseRedirect('/app/tenant_admin/')	

# invalid_login() redirects to the invalid login page
def invalid_login(request):
	return render_to_response('app/invalid_login.html')

# logout() view terminates the user session and logs it out of the
# system.

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/app/login')

# tenant_admin() fetches the details required to be populated on the 
# tenant_admin page by quering the database if the user has logged in
# successfully
def tenant_admin(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	userdetails=User_More.objects.get(user_id=request.user.id)
	tenantdetails=Tenant.objects.get(pk=userdetails.tenant_id)
	userType=User_Type.objects.filter(tenant_id=userdetails.tenant_id)
	userAll=User_More.objects.filter(tenant_id=userdetails.tenant_id)
	return render_to_response('app/tenant_admin.html',{'user':request.user, 'tenant' : tenantdetails, 'userType' : userType, 'userAll':userAll})

# standard_user() fetches the details required to be populated on the 
# standard_user page by quering the database if the user has logged in 
# successfully
def standard_user(request):
	c={}
	c.update(csrf(request))
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	userdetails=User_More.objects.get(user_id=request.user.id)
	tenantdetails=Tenant.objects.get(pk=userdetails.tenant_id)
	userType=User_Type.objects.get(tenant_id=userdetails.tenant_id,userType=unicode('N'))
	
	fileDetails = cache.get(USER_FILES)
	if not fileDetails:
		fileDetails = File.objects.filter(user_id=request.user.id) 
	counter = 0
	maxSizeCounterGB = userType.maxStorage
	maxSizeCounter = float(maxSizeCounterGB)*1024*1024*1024
	maxSizeFileMB = userType.maxSize
	maxSizeFileCounter = float(maxSizeFileMB)*1024*1024
	for files in fileDetails:
		counter = counter + files.upfile.size
		files.upfile.filename=files.upfile.name.split("/")[-1]
	
	if request.method == 'POST':		
		allowedExt=userType.allowedExt
		allowedExt=allowedExt.split(",")
		ufile=request.FILES['docfile'].name.split(".")[-1]
		uFileSize = request.FILES['docfile'].size
		if ufile not in allowedExt:
			return render_to_response('app/error.html')
		if 	(uFileSize + counter) > maxSizeCounter:
			return render_to_response('app/error.html')
		if request.FILES['docfile'].size > maxSizeFileCounter:
		 	return render_to_response('app/error.html')
		newdoc = File(user_id=request.user.id, tenant_id=userdetails.tenant_id, upfile = request.FILES['docfile'])
		newdoc.save()
		#update the cache here
		cache.set(USER_FILES, _get_files(request.user))
		return HttpResponseRedirect('/app/loggedin')
	else:				
		#use the cache here
		return render(request,('app/standard_user.html',c),{'user':request.user, 'tenant' : tenantdetails, 'userType' : userType, 'files' : fileDetails, 'sizeUsed' : counter})

# previleged_user() fetches the details required to be populated on the 
# previliged_user page by quering the database if the user had logged in the 
# successfully
def privileged_user(request):
	c={}
	c.update(csrf(request))
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')	
	
	userdetails=User_More.objects.get(user_id=request.user.id)
	tenantdetails=Tenant.objects.get(pk=userdetails.tenant_id)
	userType=User_Type.objects.get(tenant_id=userdetails.tenant_id,userType=unicode('P'))
	fileDetails = cache.get(USER_FILES)
	if not fileDetails:
		fileDetails = File.objects.filter(user_id=request.user.id)
	counter = 0
	maxSizeCounterGB = userType.maxStorage
	maxSizeCounter = float(maxSizeCounterGB)*1024*1024*1024
	maxSizeFileMB = userType.maxSize
	maxSizeFileCounter = float(maxSizeFileMB)*1024*1024
	for files in fileDetails:
		counter = counter + files.upfile.size
		files.upfile.filename=files.upfile.name.split("/")[-1]
		
	#Script to catch file and upload
	if request.method == 'POST':		
		allowedExt=userType.allowedExt
		allowedExt=allowedExt.split(",")
		ufile=request.FILES['docfile'].name.split(".")[-1].lower()
		uFileSize = request.FILES['docfile'].size
		if ufile not in allowedExt:
			return render_to_response('app/error.html')
		if 	(uFileSize + counter) > maxSizeCounter:
			return render_to_response('app/error.html')
		if request.FILES['docfile'].size > maxSizeFileCounter:
		 	return render_to_response('app/error.html')
		# elif float(counter+(request.FILES['docfile'].size)) >= float(userType.maxStorage) * 1024:
		# 	return HttpResponseRedirect('/app/privileged_user')
		newdoc = File(user_id=request.user.id, tenant_id=userdetails.tenant_id,upfile = request.FILES['docfile'])
		newdoc.save()		
		#update the cache here
		cache.set(USER_FILES, _get_files(request.user))		
		return HttpResponseRedirect('/app/privileged_user')
	else:		
		#use the cache here
		return render(request,('app/privileged_user.html',c),{'user':request.user, 'tenant' : tenantdetails, 'userType' : userType, 'files' : fileDetails, 'sizeUsed' : counter})

def _get_files(user):
	return File.objects.filter(user_id=user.id)

# superuser() fetches the details required to be populated on the 
# superuser page by quering the database if the user has logged in successfully
def superuser(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	filesAll=File.objects.all()
	tenantAll=Tenant.objects.all()
	totalTenant = Tenant.objects.all().aggregate(Max('id'))
	temp = totalTenant.values()
	countTenant = temp[0]
	sizeUsedList = [0]
	for i in range(0,countTenant):
 		sizeUsedList.append(0)
	count = 0
	for tenant in tenantAll:
		counter = 0
		for aFile in filesAll:
			if aFile.tenant_id == tenant.id:
				counter = counter + aFile.upfile.size
		sizeUsedList[tenant.id] = counter 		
	return render_to_response('app/superuser.html',{'tenants' : tenantAll, 'sizeUsedList' : sizeUsedList });

# edit_privileged_rights() redirects the tenant admin to edit the rights of the 
# previliged user if login was successfull
def edit_privileged_rights(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	c={}
	c.update(csrf(request))
	return render_to_response('app/edit_privileged_rights.html',c)

# set_privileged_rights() modifies the rights of the privileged user based on the 
# requirments submitted by tenant admin if login was successfull
def set_privileged_rights(request):
	totalSpace=request.POST.get('totalSpace', '')
	maxSize=request.POST.get('maxSize','')
	ext=request.POST.get('ext','')

	userdetails=User_More.objects.get(user_id=request.user.id)
	userType=User_Type.objects.get(tenant_id=userdetails.tenant_id,userType=unicode('P'))
	userType.maxStorage=totalSpace
	userType.maxSize=maxSize
	userType.allowedExt=ext
	userType.save()
	return HttpResponseRedirect('/app/loggedin')

# edit_standard_rights() redirects the tenant admin to edit the rights of the 
# standard user if login was successfull
def edit_standard_rights(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	c={}
	c.update(csrf(request))
	return render_to_response('app/edit_standard_rights.html',c)

# set_standard_rights() modifies the rights of the standard user based on the 
# requirments submitted by tenant admin if login was successfull
def set_standard_rights(request):
	totalSpace=request.POST.get('totalSpace', '')
	maxSize=request.POST.get('maxSize','')
	ext=request.POST.get('ext','')

	userdetails=User_More.objects.get(user_id=request.user.id)
	userType=User_Type.objects.get(tenant_id=userdetails.tenant_id,userType=unicode('N'))
	userType.maxStorage=totalSpace
	userType.maxSize=maxSize
	userType.allowedExt=ext
	userType.save()
	return HttpResponseRedirect('/app/login')

# add_tenant() allows the superuser to add a new tenant 
def add_tenant(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/loggedin')
	if request.user.id!=1:
		return render_to_response( 'app/unauthorized.html')
	c={}
	c.update(csrf(request))
	return render_to_response( 'app/add_tenant.html',c)

# save_tenant() sets the basic details of the tenant by tenant if login was successfull
def save_tenant(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/loggedin')
	if request.user.id!=1:
		return render_to_response( 'app/unauthorized.html')
	
	tenantName=request.POST.get('name', '')
	space=request.POST.get('space', '')
	
	adminName=request.POST.get('adminname', '')
	email=request.POST.get('email', '')
	fname=request.POST.get('fname', '')
	lname=request.POST.get('lname', '')
	password=request.POST.get('password', '')

	tenant=Tenant(name=tenantName,space=space)
	tenant.save()
	tenantid=tenant.id

	usr=User.objects.create_user(username=adminName,password=password,email=email,first_name=fname,last_name=lname)
	usr.save()
	usrid=usr.id

	usrtypeA=User_Type(tenant_id=tenantid,userType='A',maxSize='-',maxStorage='-',allowedExt='-')
	usrtypeA.save()

	usrtypeN=User_Type(tenant_id=tenantid,userType='N',maxSize='-',maxStorage='-',allowedExt='-')
	usrtypeN.save()

	usrtypeP=User_Type(tenant_id=tenantid,userType='P',maxSize='-',maxStorage='-',allowedExt='-')
	usrtypeP.save()

	usrmore=User_More(user_id=usrid,tenant_id=tenantid,userType_id=usrtypeA.uTypeId)
	usrmore.save()

	return HttpResponseRedirect('/app/loggedin')

# edit_tenant() helps the tenant change its details if the login was sucessfull
def edit_tenant(request,tenant):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	if request.user.id!=1:
		return render_to_response( 'app/unauthorized.html')
	c={}
	c.update(csrf(request))
	tenant=Tenant.objects.get(pk=tenant)
	userType=User_Type.objects.get(tenant_id=tenant.id,userType='A')
	
	tenantAdmin=User_More.objects.get(tenant_id=tenant.id, userType_id=userType.uTypeId)
	
	user=User.objects.get(pk=tenantAdmin.user_id)

	return render(request,('app/edit_tenant.html', c),{'tenant':tenant, 'admin' : user})

def update_tenant(request,tenant):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	if request.user.id!=1:
		return render_to_response( 'app/unauthorized.html')
	tenant=Tenant.objects.get(pk=tenant)
	space=request.POST.get('space', '')
	
	adminname=request.POST.get('adminname', '')
	email=request.POST.get('email', '')
	fname=request.POST.get('fname', '')
	lname=request.POST.get('lname', '')
	password=request.POST.get('password', '')

	tenant.space=space
	tenant.save()
	userType=User_Type.objects.get(tenant_id=tenant.id,userType='A')
	tenantAdmin=User_More.objects.get(tenant_id=tenant.id, userType_id=userType.uTypeId)
	#tenantAdmin.user.username=adminname
	tenantAdmin.user.first_name=fname
	tenantAdmin.user.last_name=lname
	tenantAdmin.user.email=email
	tenantAdmin.user.set_password(password)
	tenantAdmin.user.save()
	return HttpResponseRedirect('/app/loggedin')

	
# create_user() helps the tenant admin create new user of different type like standard 
# or previliged if login was successfull
def create_user(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	c={}
	c.update(csrf(request))
	return render_to_response('app/create_user.html',c)	


def creating_user(request):	
	userType=request.POST.get('userType','')
	fName=request.POST.get('fName', '')
	lName=request.POST.get('lName', '')
	email=request.POST.get('email', '')
	username=request.POST.get('username', '')
	password=request.POST.get('password', '')
	user=User.objects.create_user(first_name=fName, last_name=lName, email=email, username=username, password=password)
	user.save()
	tenantAdmin=User_More.objects.get(user_id=request.user.id)
	usertype=User_Type.objects.get(tenant_id=tenantAdmin.tenant_id, userType=userType)	

	userdetails=User_More(tenant_id=tenantAdmin.tenant_id,user_id=user.id,userType_id=usertype.uTypeId)
	userdetails.save()
	return HttpResponseRedirect('/app/user_created')

def user_created(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	c={}
	c.update(csrf(request))	
	return render_to_response('app/user_created.html',c)

def delete_file_p(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	c={}
	c.update(csrf(request))
	if request.method=='POST':
		file_id = int(request.POST.get('file_id', ''))
		fileToDelete = File.objects.get(pk=file_id)		
		fileToDelete.delete()
		cache.set(USER_FILES, _get_files(request.user))
		return HttpResponseRedirect('/app/privileged_user')		

def delete_file_s(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/app/login')
	c={}
	c.update(csrf(request))
	if request.method=='POST':
		file_id = int(request.POST.get('file_id', ''))
		fileToDelete = File.objects.get(pk=file_id)	
		fileToDelete.delete()
		cache.set(USER_FILES, _get_files(request.user))
		return HttpResponseRedirect('/app/standard_user')		