from rest_framework import serializers
from users.models import CustomUser

class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, value):
        try:
            CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist: 
            raise serializers.ValidationError("This user does not exist.")
        return value
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    def validate_correct_current_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect Password.")
        return value
    



    
