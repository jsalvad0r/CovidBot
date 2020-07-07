from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from tamizaje.constants import (DNI_DOCUMENT, DOCUMENTO_TYPE_CHOICES,
                                FEMALE_RISK, GENDER_CHOICES, MALE_GENDER,
                                MALE_RISK)


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
    YES_NO_CHOICES = (
        (True, 'Si'),
        (False, 'No')
    )
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    have_hypertension = models.BooleanField(default=False)
    have_diabetes = models.BooleanField(default=False)
    is_smoker = models.BooleanField(default=False)
    have_respiratory_distress_syndrome = models.BooleanField(default=False)
    have_heart_disease = models.BooleanField(default=False)
    have_inmunosupression = models.BooleanField(default=False)
    had_contact_covid = models.BooleanField(default=False, choices=YES_NO_CHOICES)
    symptons = models.CharField(blank=True, null=True, max_length=200)  

    class Meta:
        abstract = True
    
    def __str__(self):
        return str(self.person)


class SupectedPatient(models.Model):
    death_rate_covid19 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True) 
    is_positive = models.BooleanField(default=False)
    test_at = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True


class Patient(BasePatient, SupectedPatient):
    
    def calculate_death_rate_covid(self):
        result = 0.001
        data_base = []
        age = self.person.age_year
        age = age if age <= 99 else 99

        if self.person.gender == MALE_GENDER:
            data_base = MALE_RISK
            result += MALE_RISK[age].get('base')
        else:
            data_base = FEMALE_RISK
            result += FEMALE_RISK[age].get('base')
        if self.have_hypertension:
            result += data_base[age].get('hipertension')
        if self.have_diabetes:
            result += data_base[age].get('diabetes')
        if self.is_smoker:
            result += data_base[age].get('fumador')
        if self.have_respiratory_distress_syndrome:
            result += data_base[age].get('pRespiratorios')
        if self.have_heart_disease:
            result += data_base[age].get('pCardiovasculares')
        if self.have_inmunosupression:
            result += data_base[age].get('inmunosupresion')
        if result >=1:
            result = 0.9999
        self.death_rate_covid19 = result * 100
        self.save()
    
    @property
    def risk_level(self):
        if self.death_rate_covid19 < 50.00:
            return 'Bajo'
        elif self.death_rate_covid19 >= 50 and self.death_rate_covid19 < 80.00:
            return 'Intermedio'
        elif self.death_rate_covid19 >= 80.00:
            return 'Alto'
    
    @property
    def risk_factors_display(self):
        risks = []
        if self.have_hypertension:
            risks.append('Hipertensión')
        if self.have_diabetes:
            risks.append('Diabetes')
        if self.is_smoker:
            risks.append('Fumador')
        if self.have_respiratory_distress_syndrome:
            risks.append('Problemas respiratorios')
        if self.have_heart_disease:
            risks.append('Problemas cardiovasculares')
        if self.have_inmunosupression:
            risks.append('Inmunosupresión')
        return ', '.join(risks)
