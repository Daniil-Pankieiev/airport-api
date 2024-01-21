from django.contrib import admin

from airport.models import (
    Flight,
    Order,
    Ticket,
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Ticket)
