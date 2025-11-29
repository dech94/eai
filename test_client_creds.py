import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_eai.settings')
django.setup()

from simulation.models import Client

# Create a new client
client = Client.objects.create(name="Test Client", base_url="http://example.com")
print(f"Client created: {client.name}")
print(f"Client ID: {client.client_id}")
print(f"Client Secret: {client.client_secret}")

if client.client_id and client.client_secret:
    print("SUCCESS: Credentials generated.")
else:
    print("FAILURE: Credentials missing.")
