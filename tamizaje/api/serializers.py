from rest_framework import serializers

from tamizaje.models import Patient


class PatientSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    document = serializers.SerializerMethodField()
    full_name = serializers.CharField(source="person.full_name")
    gender = serializers.CharField(source="person.get_gender_display")
    age = serializers.CharField(source="person.age_year")
    photo = serializers.CharField(source="person.photo")
    distance = serializers.CharField(default="")
    duration = serializers.CharField(default="")
    phone_number = serializers.CharField(source='person.phone_number')
    had_contact_covid = serializers.CharField(source='get_had_contact_covid_display')

    class Meta:
        model = Patient
        fields = (
            'death_rate_covid19', 'document',
            'full_name', 'gender', 'address',
            'age', 'photo', 'distance', 'duration',
            'phone_number', 'risk_factors_display',
            'symptons', 'had_contact_covid'
        )
    
    def get_address(self, obj):
        return str(obj.person.address_set.first())
    
    def get_document(self, obj):
        return f'{obj.person.get_document_type_display()} - {obj.person.document_number}'
