from django.shortcuts import render, render_to_response
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect,HttpResponse
from users.models import User
from cargo_app.models import CorporateUser
from cargo_app.models import Shipment
from IPython import embed



def edituser(request, pk):
    if request.method == 'GET':
        user = User.objects.filter(id=pk)[0]
        return render_to_response('users/edituser.html', {'userid':request.COOKIES['userid'], 'user':user})
    if request.method == 'POST':
        params = request.POST
        if(User.objects.filter(email=params["mail"]).count() > 0):
            return render_to_response("users/edituser.html", {'userid':request.COOKIES['userid'], 'message':'Email has already been used.', 'messagetype':2})
        User.objects.filter(id=pk).update(name=params["uname"],
                                        surname=params["sname"],
                                        password=params["passwd"],
                                        telephone=params["telno"],
                                        email=params["mail"],
                                    )
        return render_to_response("home/home.html", {'userid':request.COOKIES['userid'], 'message':'User information has been changed', 'messagetype':1})


def adduser(request):
    if request.method == 'POST':
        params = request.POST
        if(User.objects.filter(email=params["mail"]).count() > 0):
            return render_to_response("users/adduser.html", {'userid':request.COOKIES['userid'], 'message':'Email has already been used.', 'messagetype':2})
        User.objects.create(name=params["uname"],
                            surname=params["sname"],
                            password=params["passwd"],
                            telephone=params["telno"],
                            email=params["mail"],
                            )        
        return render_to_response("home/home.html", {'userid':request.COOKIES['userid'], 'message':'A new User Created', 'messagetype':1})
    elif request.method == 'GET':
        return render(request, "users/adduser.html",{'userid':request.COOKIES['userid']})



def register(request):
    if request.method == 'POST':
        params = request.POST
        if(User.objects.filter(email=params["mail"]).count() > 0):
            return render_to_response("users/register.html", {'firms':CorporateUser.objects.all(),'message':'Email has already been used.', 'messagetype':2})
        User.objects.create(name=params["uname"],
                            surname=params["sname"],
                            password=params["passwd"],
                            telephone=params["telno"],
                            email=params["mail"],
                            )        
        return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'message':'You are registered', 'messagetype':1})
    elif request.method == 'GET':
        return render(request, "users/register.html")

def login(request):
    if 'userid' in request.COOKIES:
        return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'message':'Already login', 'messagetype':2})
    if request.method == 'POST':
        params = request.POST
        filtered_query = User.objects.filter(email=params['mail'])
        if(filtered_query.count() == 1 and filtered_query[0].password == params['passwd']):
            response = render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'userid':filtered_query[0].id, 'message':'Successful Login', 'messagetype':1})
            response.set_cookie('userid', filtered_query[0].id)
            # response.cookies.get('userid') <Morsel: userid=15; Path=/>
            return response
        else:
            return render_to_response("users/login.html", {'message':'Invalid email or password', 'messagetype':2})
    elif request.method == 'GET' :
        return render(request, "users/login.html")
def details(request,pk):
    if request.method == 'GET':
        return render_to_response("users/details.html", {'userid':request.COOKIES['userid'], 'User':User.objects.filter(id=pk)[0]})
    elif request.method == 'POST':
        params = request.POST
        User.objects.filter(id=pk).update(name=params['uname'],
                                    surname=params['sname'],
                                    password=params['passwd'],
                                    email=params['mail'],
                                    telephone=params['telno'],
                                    )
        
        return render(request, "home/home.html", {'firms':CorporateUser.objects.all(),'userid':request.COOKIES['userid'], 'message':'Changes Saved','messagetype':1})
def logout(request):
    response = render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'message':'Successful Logout', 'messagetype':1})
    response.delete_cookie('userid')
    return response

def delete(request, pk):
    if request.COOKIES['userid'] != pk:
        User.objects.filter(id=pk).delete()
    return render_to_response('adminpanel/index.html', {'userid':request.COOKIES['userid'], 'shipmentList':list(Shipment.objects.all()), 'userList':list(User.objects.all())})

def update(request, pk):
    if request.method == 'GET':
        user = User.objects.filter(id=pk)[0]
        return render_to_response('users/profile.html', {'userid':request.COOKIES['userid'], 'user':user})
    if request.method == 'POST':
        embed()
        params = request.POST
        if(User.objects.filter(email=params["mail"]).count() > 0):
            return render_to_response("users/profile.html", {'message':'Email has already been used.', 'messagetype':2})
        User.objects.filter(id=pk).update(name=params["uname"],
                                        surname=params["sname"],
                                        password=params["passwd"],
                                        telephone=params["telno"],
                                        email=params["mail"],
                                    )
        return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'userid':request.COOKIES['userid'],'message':'User information has been changed', 'messagetype':1})

def makeadmin(request, pk):
    User.objects.filter(id=pk).update(isAdmin = True)
    return render_to_response('adminpanel/index.html', {'userid':request.COOKIES['userid'], 'shipmentList':list(Shipment.objects.all()), 'userList':list(User.objects.all())})