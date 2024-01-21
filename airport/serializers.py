from django.db import transaction
from rest_framework import serializers
from .models import Airport, Route, Crew, Ticket, Order, Airplane, AirplaneType, Flight


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = (
            "name",
            "closest_big_city",
        )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = (
            "source",
            "destination",
            "distance"
        )


class RouteListSerializer(RouteSerializer):
    class Meta:
        model = Route
        fields = (
            "id",
            "full_route",
        )


class AirportListSerializer(AirportSerializer):
    source_routes = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_route"
    )

    class Meta:
        model = Airport
        fields = ("name", "closest_big_city", "source_routes")


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = (
            "source",
            "destination",
            "distance",
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = (
            "first_name",
            "last_name"
        )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("name",)


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
            "image",
        )


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(source="airplane_type.name", read_only=True)

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
            "image",
        )


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew"
        )


class FlightListSerializer(FlightSerializer):
    full_route = serializers.CharField(source="route.full_route", read_only=True)
    airplane = serializers.CharField(source="airplane.name", read_only=True)
    tickets_available = serializers.SerializerMethodField()
    airplane_image = serializers.ImageField(source="airplane.image", read_only=True)

    def get_tickets_available(self, obj):
        return obj.airplane.capacity - len(obj.tickets.all())

    class Meta:
        model = Flight
        fields = (
            "id",
            "full_route",
            "tickets_available",
            "departure_time",
            "arrival_time",
            "airplane",
            "airplane_image",
        )


class TakenPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(many=False, read_only=True)
    crew = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    airplane = serializers.CharField(source="airplane.name", read_only=True)
    airplane_image = serializers.ImageField(source="airplane.image", read_only=True)
    taken_places = TakenPlacesSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = Flight
        fields = (
            "route",
            "departure_time",
            "arrival_time",
            "airplane",
            "airplane_image",
            "crew",
            "taken_places",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        Ticket.validate_seat(
            attrs["row"],
            attrs["seat"],
            attrs["flight"],
            serializers.ValidationError,
        )

        return data

    class Meta:
        model = Ticket
        fields = ("row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", [])
        order = Order.objects.create(**validated_data)
        tickets = [Ticket(order=order, **ticket_data) for ticket_data in tickets_data]
        Ticket.objects.bulk_create(tickets)
        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=False,
    )


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")
