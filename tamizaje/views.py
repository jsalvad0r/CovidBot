from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from tamizaje.models import Patient
from django.views.generic import TemplateView
from tamizaje.services import CitizenAPI

class PatientView(TemplateView):
    template_name = 'patient/index.html'

@csrf_exempt
def webhook(request):
    req = json.loads(request.body)
    action = req.get('queryResult').get('action')
    parameters = req.get('queryResult').get('parameters')
    # if action == 'input-welcome':
    document_number = parameters.get('any')[0]
    phone_number = parameters.get('phone-number')
    address = parameters.get('address')
    birthdate = parameters.get('date').split('T')[0]
    suspected_patient = CitizenAPI.search(document_number, birthdate)
    fulfillmentText = {'fulfillmentText': f'Sr(a) {str(suspected_patient)} su solicitud a sido registrada correctamente espere a que un personal de salud se comunique con usted. Gracias, que se mejore.'}
    return JsonResponse(fulfillmentText, safe=False)