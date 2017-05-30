from django.shortcuts import render, render_to_response
from cargo_app.models import Shipment, Category
from users.models import User
from cargo_app.models import CorporateUser

def index(request):
	if 'userid' in request.COOKIES and User.objects.filter(id=int(request.COOKIES['userid']))[0].isAdmin == False:
		return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'userid':request.COOKIES['userid'], 'message':'Invalid operation.', 'messagetype':2})
	elif 'userid' not in request.COOKIES:
		return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'message':'Invalid operation.', 'messagetype':2})
	return render_to_response('adminpanel/index.html', {'userid':request.COOKIES['userid'], 'shipmentList':list(Shipment.objects.all()), 'userList':list(User.objects.all())})