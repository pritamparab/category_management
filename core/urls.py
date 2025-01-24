from django.urls import path
from core.views import ProductView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('get_products/', ProductView.as_view(), name='get_products'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout')
]

'''
from core.views import ProductView, AddToPremiumView, RemoveFromPremiumView
urlpatterns = [
    path('api/add-to-premium/', AddToPremiumView.as_view(), name='add_to_premium'),
    path('api/remove-from-premium/', RemoveFromPremiumView.as_view(), name='remove_from_premium'),,
]
'''