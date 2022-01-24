from django.urls import path
from .views import AdminFlightsViewSet, AvailableFlightsView, PassengerTicketViewSet

urlpatterns = [
    path('flights/', AdminFlightsViewSet.as_view({'get': 'list', 'post': 'create'}), name='flights'),
    path('flights/<int:pk>/',
         AdminFlightsViewSet.as_view({'get': 'retrieve', 'delete': 'destroy', 'patch': 'partial_update'}),
         name='flights_admin_exact'),

    path('flights/available/', AvailableFlightsView.as_view(), name='available_flights'),

    path('tickets/', PassengerTicketViewSet.as_view({'get': 'list', 'post': 'create'}), name='tickets'),
    path('tickets/<int:pk>/', PassengerTicketViewSet.as_view({'get': 'retrieve',
                                                              'delete': 'destroy'}), name='ticket_exact'),
]
