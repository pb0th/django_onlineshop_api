from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .serializers import RequestResetPasswordSerializer, ChangePasswordSerializer
from shared.utils.email_utils import send_reset_password_otp, generate_otp
from users.serializers import CustomUserSerializer


class AuthLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = RefreshToken(request.data["refresh"])
            refresh_token.blacklist()
            return Response({"message":"Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RequestResetPasswordView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = RequestResetPasswordSerializer(data=request.data)
        if(serializer.is_valid()):
            email = serializer.validated_data['email']
            otp = generate_otp()
            send_reset_password_otp(email=email, otp=otp)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ChangePasswordView(APIView):
   def post(self, request):
      serializer = ChangePasswordSerializer(data=request.data)
      if serializer.is_valid():
         user = request.user
         user.set_password(serializer.validated_data["new_password"])
         user.save()
         return Response({"detail":"Password updated successfully"}, status=status.HTTP_200_OK)


class UpdateProfileInfo(APIView):
    def patch(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

      
    



    
        
    