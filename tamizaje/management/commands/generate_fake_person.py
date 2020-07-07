from random import randint

from django.core.management import BaseCommand
from faker import Faker

from tamizaje.constants import GENDER_CHOICES
from tamizaje.models import Patient, Person
from tamizaje.services import Scrapper


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('total', type=int)

    def handle(self, *args, **options):
        if options['total']:
            faker = Faker()
            for i in range(options['total']):
                _gender = GENDER_CHOICES[randint(0, 1)][0]
                _risk_factor = [
                    'have_hypertension', 'have_diabetes', 'is_smoker', 
                    'have_respiratory_distress_syndrome',
                    'have_heart_disease', 'have_inmunosupression',
                    'had_contact_covid'
                ]
                _name = faker.name_male()
                if _gender == 'female':
                    _name = faker.name_female()
                person = Person.objects.create(
                    document_type='01',
                    document_number=str(faker.random_int(10000000, 99999999)),
                    name=_name,
                    first_last_name=faker.first_name(),
                    second_last_name=faker.last_name(),
                    birthdate=faker.date_of_birth(),
                    gender=_gender,
                    phone_number=faker.phone_number(),
                    photo=Scrapper.get_face_base64()
                )
                address = Scrapper.get_fake_address()
                person.address_set.create(
                    city=address.get('city'),
                    state=address.get('state'),
                    street=address.get('street')
                )
                patient = Patient.objects.create(person=person)
                setattr(patient, _risk_factor[faker.random_int(0, 6)], True)
                patient.calculate_death_rate_covid()
                self.stdout.write(self.style.SUCCESS(f'Patient generated successfully {person}'))
