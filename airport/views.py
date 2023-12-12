from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Airport, Route, Crew, Order, Airplane, AirplaneType, Flight
from .serializers import (
    AirportSerializer,
    RouteSerializer,
    CrewSerializer,
    OrderSerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    FlightSerializer,
    RouteListSerializer,
    FlightListSerializer,
    RouteDetailSerializer,
    FlightDetailSerializer,
    AirportListSerializer,
    AirplaneListSerializer,
    OrderListSerializer,
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_queryset(self):
        queryset = self.queryset
        closest_big_city = self.request.query_params.get("city")

        if closest_big_city:
            queryset = queryset.filter(closest_big_city__icontains=closest_big_city)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AirportListSerializer

        return AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer

        return AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer

    def get_queryset(self):
        queryset = self.queryset
        source_city = self.request.query_params.get("source_city")
        destination_city = self.request.query_params.get("destination_city")
        if source_city:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=source_city
            )
        if destination_city:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=destination_city
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer
class OrderPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user.id)
        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__flight__airplane",
            )
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer

        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
