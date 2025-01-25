from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
 
#from django.contrib.auth.models import Group
from core.models import Product

class CustomTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        from .serializers import CustomTokenObtainPairSerializer
        return CustomTokenObtainPairSerializer

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("User:", request.user)
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
        #accessible_categories = [cat.lower() for cat in accessible_categories]
        print("accessible_categories",accessible_categories)
        # Get products for accessible categories
        products = Product.objects.filter(category__in=accessible_categories)
        print("products",products)
        serialized_products = [
            {
                "id": product.id,
                "title": product.title,
                "price": product.price,
                "description": product.description,
                "category": product.category,
                "image_url": product.image_url,
            }
            for product in products
        ]

        return Response(serialized_products)
    
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
