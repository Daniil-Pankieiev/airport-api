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
router.register(r"airports", AirportViewSet)
router.register(r"routes", RouteViewSet)
router.register(r"crews", CrewViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"airplane-types", AirplaneTypeViewSet)
router.register(r"airplanes", AirplaneViewSet)
router.register(r"flights", FlightViewSet)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "cinema"
