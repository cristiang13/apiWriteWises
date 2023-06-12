from datetime import datetime
from django.core.mail import send_mail
from rest_framework import status
import bcrypt
from bson import ObjectId
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .authentication import CustomTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password

class RegisterView(APIView):

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        number_phone = request.data.get("phone")
        password = request.data.get("password")

        if not username or not email or not number_phone or not password:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.get_by_email(email)
        if user:
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")
         # Get the current timestamp
        timestamp = datetime.utcnow()
        user_data = {
            "username": username,
            "email": email,
            "number_phone": number_phone,
            "password": hashed_password,
            "created_at": timestamp
        }
        user_id = User.create(user_data).inserted_id
        return Response({"token": str(user_id)}, status=status.HTTP_201_CREATED)

class LoginView(APIView):

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.get_by_email(email)

        if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return Response({"error": "Incorrect username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"token": str(user["_id"]),"username": user["username"]}, status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "email required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.get_by_email(email)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token and store it in the database
        token = User.generate_password_reset_token(user["_id"])

     
        # reset_link = f"http://localhost:3000/writewiseweb/reset-password/{token}"
        reset_link = f"https://chanblock.github.io/writewiseweb/reset-password/{token}"
        send_mail(
            "Password reset request",
            f"Click the link below to reset your password:\n\n{reset_link}",
            "noreply@example.com",
            [email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):

    def put(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not token or not new_password:
            return Response({"error": "token and new_password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.collection.find_one({'password_reset_token': token})
        if not user:
            return Response({"error": "Invalid token"}, status=status.HTTP_404_NOT_FOUND)

        # Hash the new password para encriptar la clave tenerlo en cuenta para realizarlo despues 
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

        
        # Update the user's password and remove the token
        User.collection.update_one({'_id': ObjectId(user["_id"])}, {'$set': {'password': hashed_password}, '$unset': {'password_reset_token': 1}})

        return Response({"message": "Password successfully reset"}, status=status.HTTP_200_OK)
    
class ProtectedView(APIView):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view"})

