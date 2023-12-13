from datetime import timedelta

from django.utils import timezone

from airport.models import Crew, Airport, Route, AirplaneType, Airplane, Flight


def sample_airplane_type(**params):
    defaults = {
        "name": "Sampleairplanetype",
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "name": "Sampleairplane",
        "rows": 19,
        "seats_in_row": 7,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "Sampleairport",
        "closest_big_city": "Samplecity",
    }
    defaults.update(params)

    return Airport.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name="AirportSource1", closest_big_city="CitySource1")
    destination = sample_airport(
        name="AirportDestination1", closest_big_city="SitySource2"
    )
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 175,
    }
    defaults.update(params)

    return Route.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "Samplename",
        "last_name": "SampleSurname",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_flight(**params):
    defaults = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": timezone.now(),
        "arrival_time": timezone.now() + timedelta(hours=7),
    }
    defaults.update(params)
    crew = sample_crew()
    flight = Flight.objects.create(**defaults)
    flight.crew.set([crew])
    return flight
