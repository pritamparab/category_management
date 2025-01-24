from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from core.models import Product

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_groups = request.user.groups.all()
        accessible_categories = set()

        # Gather categories based on group permissions
        for group in user_groups:
            accessible_categories.update(
                group.permissions.filter(codename__startswith='access_').values_list('codename', flat=True)
            )
        print("accessible_categories 1", accessible_categories)
        accessible_categories = [
            codename.replace('access_', '').replace('_', ' ')
            for codename in accessible_categories
        ]
        print("accessible_categories 1", accessible_categories)

        # Get products for accessible categories
        products = Product.objects.filter(category__in=accessible_categories)
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

'''
class AddToPremiumView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not request.user.groups.exists():
            return Response({'error': 'You must belong to a group to access premium.'}, status=403)

        premium_group, _ = Group.objects.get_or_create(name='Premium')
        premium_group.user_set.add(request.user)
        return Response({'message': 'Added to premium successfully.'})

class RemoveFromPremiumView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        premium_group = Group.objects.filter(name='Premium').first()
        if premium_group:
            premium_group.user_set.remove(request.user)
        return Response({'message': 'Removed from premium.'})
'''