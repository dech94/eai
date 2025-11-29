from django.core.management.base import BaseCommand
from simulation.models import Pole, Sector, Bed
import random

class Command(BaseCommand):
    help = 'Initialize the hospital structure'

    def handle(self, *args, **kwargs):
        hospital_structure = {
            "Pôle Cardiologie et Vasculaire": [
                "USIC (Soins Intensifs Cardio)",
                "Explorations Fonctionnelles",
                "Hospitalisation Cardiologie"
            ],
            "Pôle Neurologie": [
                "Unité Neuro-Vasculaire (AVC)",
                "Pathologies Neurologiques",
                "Explorations Neurologiques"
            ],
            "Pôle Pneumologie": [
                "Pathologies Respiratoires",
                "Soins Continus Pneumologie",
                "Hôpital de Jour Pneumo"
            ],
            "Pôle Diabétologie - Endocrinologie": [
                "Hospitalisation Diabétologie",
                "Éducation Thérapeutique",
                "Hôpital de Jour Diabéto"
            ],
            "Pôle Gastro-entérologie": [
                "Pathologies Digestives",
                "Endoscopie Digestive",
                "Hépatologie"
            ],
            "Pôle Néphrologie et Dialyse": [
                "Centre d'Hémodialyse",
                "Dialyse Péritonéale",
                "Néphrologie Clinique"
            ],
            "Pôle Médecine Polyvalente": [
                "Médecine Polyvalente",
                "Médecine Interne",
                "Maladies Infectieuses"
            ],
            "Pôle Rhumatologie": [
                "Pathologies Osseuses",
                "Pathologies Articulaires",
                "Hôpital de Jour Rhumato"
            ],
            "Pôle Oncologie": [
                "Hôpital de Jour Onco",
                "Oncologie Médicale",
                "Soins de Support"
            ],
            "Pôle Addictologie": [
                "ELSA (Équipe de Liaison)",
                "Hospitalisation Addictologie",
                "Consultations Addictologie"
            ],
            "Pôle Chirurgie Orthopédique": [
                "Orthopédie A (Membres Inf.)",
                "Orthopédie B (Membres Sup.)",
                "Traumatologie"
            ],
            "Pôle Chirurgie Viscérale": [
                "Chirurgie Viscérale A",
                "Chirurgie Digestive",
                "Chirurgie Bariatrique"
            ],
            "Pôle Urologie": [
                "Hospitalisation Urologie",
                "Chirurgie Ambulatoire Uro",
                "Endoscopie Urologique"
            ],
            "Pôle Femme-Mère-Enfant": [
                "Maternité",
                "Néonatologie",
                "Gynécologie Obstétrique",
                "Pédiatrie Générale"
            ],
            "Pôle Chirurgie Spécialités": [
                "ORL et Chirurgie Cervico-faciale",
                "Ophtalmologie",
                "Chirurgie Plastique"
            ],
            "Pôle Anesthésie-Bloc": [
                "Bloc Opératoire Central",
                "SSPI (Salle de Réveil)",
                "Consultation Anesthésie"
            ],
            "Pôle Urgences et Soins Critiques": [
                "SAU (Urgences Adultes)",
                "SMUR",
                "UHCD (Lits Porte)",
                "Surveillance Continue (USC)"
            ],
            "Pôle Gériatrie": [
                "Court Séjour Gériatrique",
                "SSR Gériatrique",
                "USLD (Longue Durée)",
                "EHPAD",
                "UCC (Cognitivo-Comportementale)"
            ],
            "Pôle Réadaptation (MPR)": [
                "Hospitalisation MPR",
                "Plateau Technique Rééduc",
                "Hôpital de Jour MPR"
            ]
        }

        for pole_name, sectors in hospital_structure.items():
            pole_id = f"pole-{pole_name.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a').replace('(', '').replace(')', '').replace('ô', 'o').replace('î', 'i').replace('û', 'u').replace('ç', 'c')}"
            pole, created = Pole.objects.get_or_create(name=pole_name, fhir_id=pole_id)
            if created:
                self.stdout.write(f"Created Pole: {pole_name}")

            for sector_name in sectors:
                sector_id = f"{pole_id}-{sector_name.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a').replace('(', '').replace(')', '').replace('ô', 'o').replace('î', 'i').replace('û', 'u').replace('ç', 'c')}"
                sector, created = Sector.objects.get_or_create(name=sector_name, fhir_id=sector_id, pole=pole)
                if created:
                    self.stdout.write(f"  Created Sector: {sector_name}")

                # Create Beds (Locations) - 8 to 15 beds per sector
                num_beds = random.randint(8, 15)
                for i in range(1, num_beds + 1):
                    bed_num = f"{sector_name[:3].upper()}{i:02d}" 
                    bed_id = f"{sector_id}-bed-{i}"
                    bed, created = Bed.objects.get_or_create(name=f"Lit {bed_num}", fhir_id=bed_id, sector=sector)
