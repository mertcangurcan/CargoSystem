from django.shortcuts import render
from cargo_system.settings import STATIC_URL
from cargo_app.models import CorporateUser
## from users.models import Users



def index(request):
    return render(request, 'home/home.html',{'firms':CorporateUser.objects.all()}) 




    #def details(request, pk): {'userid':request.COOKIES['userid']}
    #return render_to_response('shipments/details.html', {'userid':request.COOKIES['userid'], 'shipment':Shipment.objects.filter(id=pk)[0]})