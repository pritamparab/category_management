from django.urls import path
from core.views import ProductView, LogoutView, CustomTokenObtainPairView, SignupView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('get_products/', ProductView.as_view(), name='get_products'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup')
] 
