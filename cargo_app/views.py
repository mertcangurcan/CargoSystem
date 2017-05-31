import datetime
import hashlib
import requests
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from cargo_app.models import Shipment, Category
from users.models import User
from IPython import embed
from rest_framework.decorators import api_view
from .serializers import CategorySerializer
from .models import CorporateShipment, CorporateUser
from rest_framework.test import APIClient


def sendCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)    
     
@api_view(['POST'])
def shipOrder(request):
    if request.method == 'POST':
        bank_receiptID =request.data['billNo']
    
        if checkPayment(bank_receiptID):
            last = CorporateShipment.objects.create(corporateID=CorporateUser.objects.filter(name=request.data['CompanyName'])[0], 
                                                customer_name = request.data['destname'], 
                                                customer_surname = request.data['destsurname'],
                                                source_address = "Deuzon Logistics",
                                                destination_address = request.data['Destaddress'],
                                                categoryID = calculatePrice(request.data['totalQuantity'])[1],
                                                sending_date = datetime.date.today(),
                                                trackID = "last")
            track_code = hashlib.md5()
            track_code.update(str(last.id).encode())
            track_code.digest()
            track_number = str(track_code.hexdigest()[:12].upper())
            CorporateShipment.objects.filter(id=last.id).update(trackID=track_number)
            return HttpResponse(track_number)
        #else:
        #    return None#?
        else:
            return None

def checkPayment(bank_receiptID):
    url = 'http://146.185.147.162/accounts/query/receipt/'
    url = url + str(bank_receiptID)+ '/'
    r = requests.get(url)
    des_response = r.json()
    return des_response['IsExist']
def index(request):
    
    if request.COOKIES:
        return render_to_response('shipments/list.html', {'userid':request.COOKIES['userid'], 'shipmentList':list(Shipment.objects.filter(userID=request.COOKIES['userid']))})
    else:
        return render_to_response('shipments/list.html', {'shipmentList':list(Shipment.objects.filter(request.COOKIES['userid']))})
def addshipment(request):
    if request.method == 'POST':
        params = request.POST
        price, ctgry = calculatePrice(int(params['qnt']))
        last = Shipment.objects.create(userID=User.objects.filter(id=int(request.COOKIES['userid']))[0],
        							source_address=params['source'],
        							categoryID=ctgry,
                                    destination_address=params['dest'],
                                    sending_date=datetime.datetime.now(),
                                    trackID="asd",
                                    price=price
                                    )
    
        track_code = hashlib.md5()
        track_code.update(str(last.id).encode())
        track_code.digest()
        Shipment.objects.filter(id=last.id).update(trackID=(str(track_code.hexdigest()[:12].upper())))
        return index(request)
    if request.method == 'GET': 
        return render(request, 'shipments/new_shipment.html')

def details(request, pk):
    return render_to_response('shipments/details.html', {'userid':request.COOKIES['userid'], 'shipment':Shipment.objects.filter(id=pk)[0]})

def delete(request, pk):
    Shipment.objects.filter(id=pk).delete()
    return index(request)

def update(request, pk):
    if request.method == 'GET':
        shipment = Shipment.objects.filter(id=pk)[0]
        return render_to_response('shipments/update.html', {'userid':request.COOKIES['userid'], 'shipment':shipment, 'quantity':shipment.price / shipment.categoryID.cat_price})
    if request.method == 'POST':
        params = request.POST
        price, ctgry = calculatePrice(float(params['qnt']))
        Shipment.objects.filter(id=pk).update(source_address=params['source'],
                                    destination_address=params['dest'],
                                    categoryID=ctgry,
                                    price=price
                                    )
        return index(request)

def calculatePrice(quantity):
    quantity = int(quantity)

    price = quantity * 1 #more than 50
    ctgry = None #new category needed for more than 50
    for c in Category.objects.all().iterator():
        if ctgry == None:
            ctgry = c
        if c.quantity > quantity:
            ctgry = c
            price = quantity * c.cat_price
            break
    return price, ctgry

def gettrack(request):
    if request.method == 'POST':
        params = request.POST
        query_result = Shipment.objects.filter(trackID = params['trackid'])
        if query_result.count() == 0:
            return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'userid':request.COOKIES['userid'], 'message':'Invalid track id.', 'messagetype':2})
        else:
            return render_to_response('shipments/details.html', {'userid':request.COOKIES['userid'], 'shipment':query_result[0]})

def getcorporatetrack(request):
    if request.method == 'POST':
        params = request.POST
        query_result = CorporateShipment.objects.filter(trackID = params['trackid'])
        if query_result.count() == 0:
            return render_to_response("home/home.html", {'firms':CorporateUser.objects.all(),'userid':request.COOKIES['userid'], 'message':'Invalid track id.', 'messagetype':2})
        else:
            return render_to_response('shipments/cordetails.html', {'userid':request.COOKIES['userid'], 'shipment':query_result[0]})




def listUserShipments(request,pk):
    if request.method == 'GET':
        user_shipments = Shipment.objects.filter(userID=pk)
        
        #return render_to_response('shipments/list.html', {'userid':request.COOKIES['userid'], 'shipment':Shipment.objects.filter(userID=pk)})
        return index(request)