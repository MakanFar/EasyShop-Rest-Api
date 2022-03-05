from .views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path

router = routers.SimpleRouter()
router.register(r'shops', ShopViewSet, basename='shop')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'items', ItemViewSet, basename='item')
router.register(r'cats', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'invoiceitems', InvoiceItemViewSet, basename='invoiceitem')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]

urlpatterns += router.urls


app_name = 'apis'