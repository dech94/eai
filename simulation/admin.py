from django.contrib import admin
from .models import Client, Pole, Sector, Bed, Patient, Encounter, Observation

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_url', 'client_id', 'is_active', 'created_at')
    list_filter = ('is_active',)
    readonly_fields = ('client_id', 'client_secret')

@admin.register(Pole)
class PoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'fhir_id')

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'pole', 'fhir_id')
    list_filter = ('pole',)

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'fhir_id')
    list_filter = ('sector__pole', 'sector')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date', 'gender')
    search_fields = ('first_name', 'last_name')

@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ('patient', 'bed', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'bed__sector__pole')

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'date', 'text')
    list_filter = ('date',)
