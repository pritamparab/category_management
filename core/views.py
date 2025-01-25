from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
 
#from django.contrib.auth.models import Group
from core.models import Product

class CustomTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        from .serializers import CustomTokenObtainPairSerializer
        return CustomTokenObtainPairSerializer

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "User is not authenticated"}, status=401)
    
        user_groups = request.user.groups.all()
        accessible_categories = set()

        # Gather categories based on group permissions
        for group in user_groups:
            accessible_categories.update(
                group.permissions.filter(codename__startswith='access_').values_list('codename', flat=True)
            )

        accessible_categories = [
            codename.replace('access_', '').replace('_', ' ')
            for codename in accessible_categories
        ]

        db_categories = {
            category.strip().lower(): category
            for category in Product.objects.values_list('category', flat=True)
        }

        matched_categories = [db_categories.get(cat) for cat in accessible_categories if cat in db_categories]
        accessible_products = Product.objects.filter(category__in=matched_categories)

        #premium_products = Product.objects.filter(category="Mobile Phone")

        premium_categories = ["Mobile Phone"]

        serialized_accessible_products = [
            {
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "description": product.description,
                "category": product.category,
                "image_url": product.image_url,
            }
            for product in accessible_products if product.category not in premium_categories
        ]

        serialized_premium_products = [
            {
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "description": product.description,
                "category": product.category,
                "image_url": product.image_url,
            }
            for product in accessible_products if product.category in premium_categories
        ]

        response_data = {
            "accessible_products": serialized_accessible_products,
            "premium_products": serialized_premium_products,
        }

        return Response(response_data)
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email', '')  # Email is optional

        if not username or not password:
            return Response({"detail": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        return Response({"detail": "User created successfully."}, status=status.HTTP_201_CREATED)
