import json
import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from tqdm import tqdm

class Command(BaseCommand):
    help = 'Génère un grand jeu de données FHIR simulé en français avec une structure hospitalière réaliste'

    def handle(self, *args, **kwargs):
        # Structure des Pôles et Services (Secteurs)
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
        
        first_names = [
            "Jean", "Marie", "Pierre", "Sophie", "Michel", "Nathalie", "Thomas", "Isabelle", 
            "Nicolas", "Céline", "Lucas", "Emma", "Louis", "Chloé", "Gabriel", "Léa",
            "Arthur", "Manon", "Jules", "Camille", "Adam", "Inès", "Paul", "Sarah",
            "Hugo", "Eva", "Raphaël", "Alice", "Théo", "Juliette", "Léo", "Louise"
        ]
        
        last_names = [
            "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois", 
            "Moreau", "Laurent", "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David",
            "Bertrand", "Roy", "Girard", "Guerin", "Dupont", "Fontaine", "Rousseau", "Vincent",
            "Muller", "Lambert", "Faure", "Andre", "Mercier", "Blanc", "Garnier", "Chevalier"
        ]
        
        conditions = [
            "État stable", "Observation clinique", "Post-opératoire J1", "Soins intensifs", 
            "En attente d'examens", "Sortie prévue demain", "Fièvre inexpliquée", 
            "Douleurs thoraciques", "Rééducation fonctionnelle", "Surveillance cardiaque",
            "Insuffisance respiratoire aiguë", "Diabète déséquilibré", "Crise hypertensive",
            "Colique néphrétique", "Infection urinaire", "Pneumopathie", "AVC ischémique",
            "Fracture du col du fémur", "Appendicite aiguë", "Gastro-entérite",
            "Déshydratation", "Confusion mentale", "Soins palliatifs", "Chimiothérapie"
        ]
        
        notes_templates = [
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

        data = {"entry": []}
        
        # Create Services (Organizations) and Sectors (Locations)
        for pole_name, sectors in tqdm(hospital_structure.items(), desc="Génération des Pôles", unit="pôle"):
            pole_id = f"pole-{pole_name.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a').replace('(', '').replace(')', '').replace('ô', 'o').replace('î', 'i').replace('û', 'u').replace('ç', 'c')}"
            
            # Create Pole (Organization)
            data["entry"].append({
                "resource": {
                    "resourceType": "Organization",
                    "id": pole_id,
                    "name": pole_name,
                    "type": [{"coding": [{"code": "dept", "display": "Pôle Hospitalier"}]}]
                }
            })
            
            for sector_name in sectors:
                sector_id = f"{pole_id}-{sector_name.lower().replace(' ', '-').replace('é', 'e').replace('è', 'e').replace('ê', 'e').replace('à', 'a').replace('(', '').replace(')', '').replace('ô', 'o').replace('î', 'i').replace('û', 'u').replace('ç', 'c')}"
                
                # Create Sector (Location)
                data["entry"].append({
                    "resource": {
                        "resourceType": "Location",
                        "id": sector_id,
                        "name": sector_name,
                        "managingOrganization": {"reference": f"Organization/{pole_id}"}
                    }
                })
                
                # Create Beds (Locations) - 8 to 15 beds per sector
                num_beds = random.randint(8, 15)
                for i in range(1, num_beds + 1):
                    bed_num = f"{sector_name[:3].upper()}{i:02d}" 
                    bed_id = f"{sector_id}-bed-{i}"
                    
                    data["entry"].append({
                        "resource": {
                            "resourceType": "Location",
                            "id": bed_id,
                            "name": f"Lit {bed_num}",
                            "partOf": {"reference": f"Location/{sector_id}"},
                            "physicalType": {"coding": [{"code": "bd", "display": "Lit"}]}
                        }
                    })
                    
                    # 75% chance of having a patient
                    if random.random() < 0.75:
                        patient_id = f"patient-{bed_id}"
                        first = random.choice(first_names)
                        last = random.choice(last_names)
                        dob_year = random.randint(1935, 2010)
                        dob = f"{dob_year}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
                        condition = random.choice(conditions)
                        
                        # Patient
                        data["entry"].append({
                            "resource": {
                                "resourceType": "Patient",
                                "id": patient_id,
                                "name": [{"family": last, "given": [first]}],
                                "birthDate": dob,
                                "gender": random.choice(["male", "female"])
                            }
                        })
                        
                        # Encounter (Link Patient to Bed)
                        data["entry"].append({
                            "resource": {
                                "resourceType": "Encounter",
                                "id": f"encounter-{patient_id}",
                                "status": "in-progress",
                                "subject": {"reference": f"Patient/{patient_id}"},
                                "location": [{"location": {"reference": f"Location/{bed_id}"}}],
                                "reasonCode": [{"text": condition}]
                            }
                        })
                        
                        # Handovers (Observations/Notes) - Generate 1-4 notes
                        for _ in range(random.randint(1, 4)):
                            note_text = random.choice(notes_templates)
                            note_date = datetime.now() - timedelta(hours=random.randint(1, 72))
                            data["entry"].append({
                                "resource": {
                                    "resourceType": "Observation",
                                    "status": "final",
                                    "subject": {"reference": f"Patient/{patient_id}"},
                                    "effectiveDateTime": note_date.isoformat(),
                                    "note": [{"text": note_text}],
                                    "code": {
                                        "coding": [{
                                            "system": "http://loinc.org",
                                            "code": "11506-3",
                                            "display": "Progress note- nursing"
                                        }]
                                    }
                                }
                            })

        with open('mock_fhir_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            
        self.stdout.write(self.style.SUCCESS('Données FHIR simulées générées avec succès (Français, Structure Complète)'))
