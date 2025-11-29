
import json
import os
from django.core.management.base import BaseCommand
from django.utils import timezone
from handover.models import Service, Sector, Bed, Patient, Handover
from django.contrib.auth.models import User
import random
from django.db import transaction
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Ingest mock FHIR data'

    def handle(self, *args, **options):
        file_path = 'mock_fhir_data.json'
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f'File {file_path} not found'))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        entries = data.get('entry', [])
        
        # Second pass for Encounters and Observations to link to DB objects
        # We need to map FHIR IDs to DB objects.
        fhir_map = {} # fhir_id -> db_instance

        # Clear existing data first?
        Service.objects.all().delete()
        Sector.objects.all().delete()
        Bed.objects.all().delete()
        Patient.objects.all().delete()
        Handover.objects.all().delete()

        # Create 15 random users if they don't exist
        for i in range(1, 16):
            username = f'user{i}'
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username, 'user@example.com', 'password')
                self.stdout.write(f'Created user {username}')

        # Get all users except admin
        users = list(User.objects.exclude(is_superuser=True))
        
        entries = data.get('entry', [])
        total_entries = len(entries)

        with transaction.atomic():
            self.stdout.write("Import des structures et patients...")
            for entry in tqdm(entries, desc="Pass 1/2", unit="entry"):
                resource = entry.get('resource', {})
                resource_type = resource.get('resourceType')
                fhir_id = resource.get('id')

                if resource_type == 'Organization':
                    service = Service.objects.create(name=resource.get('name'))
                    fhir_map[fhir_id] = service
                
                elif resource_type == 'Location':
                    # Check if it's a Sector or Bed
                    if 'managingOrganization' in resource: # It's a Sector
                        org_ref = resource['managingOrganization']['reference'].split('/')[1]
                        service = fhir_map.get(org_ref)
                        if service:
                            sector = Sector.objects.create(name=resource.get('name'), service=service)
                            fhir_map[fhir_id] = sector
                    elif 'partOf' in resource: # It's a Bed
                        sector_ref = resource['partOf']['reference'].split('/')[1]
                        sector = fhir_map.get(sector_ref)
                        if sector:
                            bed = Bed.objects.create(number=resource.get('name'), sector=sector)
                            fhir_map[fhir_id] = bed

                elif resource_type == 'Patient':
                    name = resource.get('name', [{}])[0]
                    first = name.get('given', [''])[0]
                    last = name.get('family', '')
                    dob = resource.get('birthDate')
                    
                    # French medical data
                    doctors = ['Dr. Martin', 'Dr. Bernard', 'Dr. Thomas', 'Dr. Petit', 'Dr. Robert', 'Dr. Richard', 'Dr. Durand', 'Dr. Dubois']
                    conditions_history = ['Hypertension', 'Diabète', 'Asthme', 'Aucun', 'Insuffisance cardiaque', 'Cholestérol', 'Arthrose']
                    admission_reasons = ['Douleur thoracique', 'Essoufflement', 'Fièvre', 'Traumatisme', 'Douleur abdominale', 'Malaise', 'Chute']
                    
                    patient = Patient.objects.create(
                        first_name=first,
                        last_name=last,
                        date_of_birth=dob,
                        condition="N/A", # Will be updated by Encounter
                        doctor_in_charge=random.choice(doctors),
                        medical_history=random.choice(conditions_history),
                        reason_for_admission=random.choice(admission_reasons),
                        upcoming_appointments=f"{random.choice(['IRM', 'Scanner', 'Consultation', 'Échographie', 'Radio', 'Prise de sang', 'Kiné'])} : {timezone.now().date() + timezone.timedelta(days=random.randint(1, 10))}" if random.random() < 0.3 else "",
                        estimated_discharge_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 14)),
                        ambulance_notified=random.choice([True, False])
                    )
                    fhir_map[fhir_id] = patient

            self.stdout.write("Liaison des lits et création des transmissions...")
            # Second pass for Encounters (linking Patient to Bed and Condition)
            for entry in tqdm(entries, desc="Pass 2/2", unit="entry"):
                resource = entry.get('resource', {})
                resource_type = resource.get('resourceType')
                
                if resource_type == 'Encounter':
                    patient_ref = resource['subject']['reference'].split('/')[1]
                    location_ref = resource['location'][0]['location']['reference'].split('/')[1]
                    condition = resource['reasonCode'][0]['text']
                    
                    patient = fhir_map.get(patient_ref)
                    bed = fhir_map.get(location_ref)
                    
                    if patient and bed:
                        patient.bed = bed
                        patient.condition = condition
                        patient.save()

                elif resource_type == 'Observation':
                    patient_ref = resource['subject']['reference'].split('/')[1]
                    note_text = resource['note'][0]['text']
                    date_str = resource.get('effectiveDateTime')
                    
                    patient = fhir_map.get(patient_ref)
                    if patient:
                        Handover.objects.create(
                            patient=patient,
                            note=note_text,
                            author=random.choice(users) if users else None,
                            created_at=date_str if date_str else timezone.now()
                        )

        self.stdout.write(self.style.SUCCESS('Données FHIR ingérées avec succès'))
