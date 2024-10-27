from rest_framework import serializers
from .models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'display_name', 'phone_number', 'date_of_birth']

    def update(self, instance, validated_data):
        instance.display_name = validated_data.get("display_name", instance.display_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.date_of_birth = validated_data.get("date_of_birth", instance.date_of_birth)
        instance.save()
        return instance