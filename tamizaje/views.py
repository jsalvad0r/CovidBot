import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from tamizaje.models import Patient
from tamizaje.services import ReniecClient


class PatientView(TemplateView):
    template_name = 'patient/index.html'


@csrf_exempt
def webhook(request):
    req = json.loads(request.body)
    # action = req.get('queryResult').get('action')
    parameters = req.get('queryResult').get('parameters')
    # if action == 'input-welcome':
    document_number = parameters.get('any')
    phone_number = parameters.get('phone-number')
    address = parameters.get('address')
    birthdate = parameters.get('date').split('T')[0]
    padecimiento = parameters.get('padecimiento')
    had_contact_covid = parameters.get('contacto_covid')
    sintoma = parameters.get('sintoma')
    patient = Patient.objects.get(
        person__document_number=document_number, person__document_type='01'
    )
    if not patient:
        person, msg = ReniecClient.search(document_number, birthdate)
        if not person:
            return JsonResponse({
                'fulfillmentText': msg
            }, safe=True)
        patient = Patient(person=person)
    
    if not padecimiento == 'none':
        setattr(patient, padecimiento, True)
    if had_contact_covid:
        patient.had_contact_covid = True
    if sintoma:
        patient.symptons = sintoma
    person = patient.person
    person.phone_number = phone_number
    patient.save()
    patient.calculate_death_rate_covid()
    fulfillmentText = {
        'fulfillmentText': f'''
            Sr(a) {str(patient.person)} su nivel de riesgo es {patient.risk_level},
            un personal de salud se acercara a su domicilio para tomar la muestra,
            no se preocupe estamos tomando en cuenta su nivel de riesgo asi
            que trataremos de hacerle llegar la atención lo mas pronto.
            Que se mejore
        '''
    }
    return JsonResponse(fulfillmentText, safe=False)
