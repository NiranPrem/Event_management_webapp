from django.urls import path
from . import views

urlpatterns = [
    path('orderscart/', views.show_orderscart, name='orderscart'),
    path('add/<int:event_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
