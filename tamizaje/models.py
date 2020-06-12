from django.db import models
from mpi_client.client import MPIClient
from django.conf import settings
from datetime import datetime
from tamizaje.constants import DNI_DOCUMENT, DOCUMENTO_TYPE_CHOICES, GENDER_CHOICES
from django.utils.functional import cached_property

class Person(models.Model):
    document_type = models.CharField(max_length=20, choices=DOCUMENTO_TYPE_CHOICES, default=DNI_DOCUMENT)
    document_number = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    first_last_name = models.CharField(max_length=50)
    second_last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=20)
    photo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.get_document_type_display()} - {self.document_number}'
    
    @cached_property
    def full_name(self):
        return '{name} {f_last_name} {s_last_name}'.format(
            name=self.name,
            f_last_name=self.first_last_name,
            s_last_name=self.second_last_name or '')
    
    @property
    def age_year(self):
        current_date = datetime.now()
        return (current_date.year - self.birthdate.year) - int(
            (current_date.month, current_date.day) < (self.birthdate.month, self.birthdate.day)
        )

class Address(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    street = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.street} {self.city}'


class BasePatient(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    padecimientos = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return str(self.person)


class SupectedPatient(models.Model):
    nivel_riesgo = models.CharField(max_length=100, blank=True, null=True)
    is_positive = models.BooleanField(default=False)
    test_at = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class Patient(BasePatient, SupectedPatient):
    pass
