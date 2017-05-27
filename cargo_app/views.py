import datetime
import hashlib
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from cargo_app.models import Shipment, Category
from users.models import User
from IPython import embed
from rest_framework.decorators import api_view
from .serializers import CategorySerializer
from .models import CorporateShipment
from rest_framework.test import APIClient


def sendCategories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)    
     
@api_view()
def shipOrder(request):
    if request.method == 'POST':
        
        if checkPayment(request.get.data('bank_receiptID'),request.get.data('quantity')):
            last = CorporateShipment.objects.create(corporateID=CorporateUser.objects.filter(name='cname').id, 
                                            customer_name = 'customer_name', 
                                            customer_surname = 'customer_surname',
                                            source_address = 'cname',#?
                                            destination_address = request.get.data('destination_address'),
                                            categoryID = calculatePrice(request.get.data('quantity'))[1],#?
                                            sending_date = datetime.date.today(),
                                            trackID = "last",)
            track_code = hashlib.md5()
            track_code.update(str(last.id).encode())
            track_code.digest()
            track_number = str(track_code.hexdigest()[:12].upper())
            CorporateShipment.objects.filter(id=last.id).update(trackID=track_number)
            return track_number
        else:
            return None#?

@api_view()
def checkPayment(bank_receiptID, quantity):
    client = APIClient()
    bank_receipt = client.GET('/bankip/', {'receiptID':bank_receiptID}, format='json')
    if bank_receipt is not None:
        receiptID = bank_receipt.data.get('receiptID')
        price = calculatePrice(quantity)[0]
        if price == bank_receipt.data.get('price'):
            return True
        else:
            return False
    else:
        return False

def index(request):
    return render_to_response('shipments/list.html', {'userid':request.COOKIES['userid'], 'shipmentList':list(Shipment.objects.all())})

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
        #return render(request, 'shipments/update.html')
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
            return render_to_response("home/home.html", {'userid':request.COOKIES['userid'], 'message':'Invalid track id.', 'messagetype':2})
        else:
            return render_to_response('shipments/details.html', {'userid':request.COOKIES['userid'], 'shipment':query_result[0].values()})



def listUserShipments(request,pk):
    if request.method == 'GET':
        user_shipments = Shipment.objects.filter(userID=pk)
        
        return render_to_response('shipments/details.html', {'userid':request.COOKIES['userid'], 'shipment':Shipment.objects.filter(userID=pk)})