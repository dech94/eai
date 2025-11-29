import os
import django
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_eai.settings')
django.setup()

from simulation.services import run_simulation_step
from simulation.models import Patient, Encounter, Observation

print("Initial counts:")
print(f"Patients: {Patient.objects.count()}")
print(f"Encounters: {Encounter.objects.count()}")
print(f"Observations: {Observation.objects.count()}")

print("Running 5 simulation steps...")
for _ in range(5):
    run_simulation_step()
    time.sleep(0.1)

print("Final counts:")
print(f"Patients: {Patient.objects.count()}")
print(f"Encounters: {Encounter.objects.count()}")
print(f"Observations: {Observation.objects.count()}")
