import random
import requests
import json
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Patient, Encounter, Observation, Bed, Client

FIRST_NAMES = [
    "Jean", "Marie", "Pierre", "Sophie", "Michel", "Nathalie", "Thomas", "Isabelle", 
    "Nicolas", "Céline", "Lucas", "Emma", "Louis", "Chloé", "Gabriel", "Léa",
    "Arthur", "Manon", "Jules", "Camille", "Adam", "Inès", "Paul", "Sarah",
    "Hugo", "Eva", "Raphaël", "Alice", "Théo", "Juliette", "Léo", "Louise"
]

LAST_NAMES = [
    "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", 
    "Moreau", "Laurent", "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David",
    "Bertrand", "Roy", "Girard", "Guerin", "Dupont", "Fontaine", "Rousseau", "Vincent",
    "Muller", "Lambert", "Faure", "Andre", "Mercier", "Blanc", "Garnier", "Chevalier"
]

CONDITIONS = [
    "État stable", "Observation clinique", "Post-opératoire J1", "Soins intensifs", 
    "En attente d'examens", "Sortie prévue demain", "Fièvre inexpliquée", 
    "Douleurs thoraciques", "Rééducation fonctionnelle", "Surveillance cardiaque",
    "Insuffisance respiratoire aiguë", "Diabète déséquilibré", "Crise hypertensive",
    "Colique néphrétique", "Infection urinaire", "Pneumopathie", "AVC ischémique",
    "Fracture du col du fémur", "Appendicite aiguë", "Gastro-entérite",
    "Déshydratation", "Confusion mentale", "Soins palliatifs", "Chimiothérapie"
]

NOTES_TEMPLATES = [
    "Patient calme, nuit sans incident notable.",
    "Douleur signalée à 4/10, antalgiques administrés avec efficacité.",
    "A voir avec le médecin référent pour validation de la sortie.",
    "Surveillance des constantes toutes les 4h, stable pour le moment.",
    "Famille prévenue de l'hospitalisation, viendra cet après-midi.",
    "Résultats sanguins reçus : légère anémie à surveiller.",
    "Bonne prise alimentaire ce midi, hydratation correcte.",
    "Pansement refait par l'IDE, cicatrice propre et non inflammatoire.",
    "Séance de kinésithérapie effectuée, bonne participation du patient.",
    "Sommeil agité, a nécessité une réassurance verbale.",
    "En attente du scanner thoracique prévu à 14h.",
    "Consultation cardiologique demandée pour avis.",
    "Patient anxieux concernant son intervention de demain.",
    "Perfusion reposée suite à une obstruction.",
    "Saturation en oxygène stable sous 2L/min."
]

def notify_clients(resource_type, resource_data):
    clients = Client.objects.filter(is_active=True)
    for client in clients:
        try:
            headers = {
                'Content-Type': 'application/json',
                'X-Client-ID': client.client_id,
                'X-Client-Secret': client.client_secret
            }
            
            # Construct full URL
            url = f"{client.base_url.rstrip('/')}/api/webhook/fhir"
            
            # Wrap in a Bundle or just send the resource? 
            # User asked to "simulate FHIR flows", so sending the resource is fine, or a bundle.
            # Let's send the raw resource for now.
            response = requests.post(url, json=resource_data, headers=headers, timeout=5)
            print(f"Sent {resource_type} to {client.name} ({url}): {response.status_code}")
        except Exception as e:
            print(f"Failed to send to {client.name}: {e}")

def create_patient_and_admit():
    # Find a free bed
    free_beds = Bed.objects.filter(encounter__isnull=True) | Bed.objects.filter(encounter__status='finished')
    # Actually, we need to check if there is an active encounter for the bed.
    # A bed is free if it has NO active encounter.
    active_encounters = Encounter.objects.filter(status='in-progress').values_list('bed_id', flat=True)
    free_beds = Bed.objects.exclude(id__in=active_encounters)

    if not free_beds.exists():
        print("No free beds available.")
        return

    bed = random.choice(list(free_beds))

    # Create Patient
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    dob_year = random.randint(1935, 2010)
    dob = f"{dob_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    
    patient = Patient.objects.create(
        first_name=first,
        last_name=last,
        birth_date=dob,
        gender=random.choice(["male", "female"])
    )

    # Create FHIR Patient Resource
    patient_resource = {
        "resourceType": "Patient",
        "id": patient.fhir_id,
        "name": [{"family": last, "given": [first]}],
        "birthDate": dob,
        "gender": patient.gender
    }
    notify_clients("Patient", patient_resource)

    # Create Encounter
    encounter = Encounter.objects.create(
        patient=patient,
        bed=bed,
        status='in-progress'
    )

    # Create FHIR Encounter Resource
    encounter_resource = {
        "resourceType": "Encounter",
        "id": encounter.fhir_id,
        "status": "in-progress",
        "subject": {"reference": f"Patient/{patient.fhir_id}"},
        "location": [{"location": {"reference": f"Location/{bed.fhir_id}"}}],
        "reasonCode": [{"text": random.choice(CONDITIONS)}]
    }
    notify_clients("Encounter", encounter_resource)
    
    print(f"Admitted {patient} to {bed}")

def discharge_patient():
    # Find active encounters
    active_encounters = Encounter.objects.filter(status='in-progress')
    if not active_encounters.exists():
        return

    encounter = random.choice(list(active_encounters))
    encounter.status = 'finished'
    encounter.end_time = timezone.now()
    encounter.save()

    # Create FHIR Encounter Resource (Update)
    encounter_resource = {
        "resourceType": "Encounter",
        "id": encounter.fhir_id,
        "status": "finished",
        "subject": {"reference": f"Patient/{encounter.patient.fhir_id}"},
        "period": {"end": encounter.end_time.isoformat()}
    }
    notify_clients("Encounter", encounter_resource)
    print(f"Discharged {encounter.patient}")

def add_observation():
    # Find active encounters
    active_encounters = Encounter.objects.filter(status='in-progress')
    if not active_encounters.exists():
        return

    encounter = random.choice(list(active_encounters))
    note_text = random.choice(NOTES_TEMPLATES)

    observation = Observation.objects.create(
        patient=encounter.patient,
        encounter=encounter,
        text=note_text
    )

    # Create FHIR Observation Resource
    observation_resource = {
        "resourceType": "Observation",
        "id": observation.fhir_id,
        "status": "final",
        "subject": {"reference": f"Patient/{encounter.patient.fhir_id}"},
        "effectiveDateTime": observation.date.isoformat(),
        "note": [{"text": note_text}],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "11506-3",
                "display": "Progress note- nursing"
            }]
        }
    }
    notify_clients("Observation", observation_resource)
    print(f"Added observation for {encounter.patient}")

def run_simulation_step():
    actions = [create_patient_and_admit, discharge_patient, add_observation]
    # Weights: More likely to add observation than admit/discharge
    weights = [0.2, 0.1, 0.7] 
    
    action = random.choices(actions, weights=weights, k=1)[0]
    action()
