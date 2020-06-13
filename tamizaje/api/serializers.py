from rest_framework import serializers
from tamizaje.models import Patient, Person

class PatientSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    document_type = serializers.CharField(source="person.get_document_type_display")
    document_number = serializers.CharField(source="person.document_number")
    full_name = serializers.CharField(source="person.full_name")
    gender = serializers.CharField(source="person.get_gender_display")
    age = serializers.CharField(source="person.age_year")
    photo = serializers.CharField(source="person.photo")
    distance = serializers.CharField(default="")
    duration = serializers.CharField(default="")

    class Meta:
        model = Patient
        fields = (
            'document_type', 'document_number',
            'full_name', 'gender', 'address',
            'age', 'photo', 'distance', 'duration'
        )
    
    def get_address(self, obj):
        return str(obj.person.address_set.first())