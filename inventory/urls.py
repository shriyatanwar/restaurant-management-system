from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IngredientViewSet, MenuItemIngredientViewSet, StockTransactionViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet, basename='ingredient')
router.register(r'menu-ingredients', MenuItemIngredientViewSet, basename='menuitemingredient')
router.register(r'transactions', StockTransactionViewSet, basename='stocktransaction')

urlpatterns = [
    path('', include(router.urls)),
]
