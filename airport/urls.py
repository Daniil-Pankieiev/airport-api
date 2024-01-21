from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AirportViewSet,
    RouteViewSet,
    CrewViewSet,
    OrderViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    FlightViewSet,
)

router = DefaultRouter()
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("orders", OrderViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("flights", FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "airport"
