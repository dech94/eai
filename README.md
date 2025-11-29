# Hospital EAI Simulator

Ce projet est un simulateur EAI (Enterprise Application Integration) pour un hôpital. Il génère des flux de données FHIR (Patient, Encounter, Observation) simulant l'activité hospitalière (admissions, sorties, notes infirmières) et les envoie à des clients connectés via des webhooks.

## Prérequis

- Python 3.8+
- pip

## Installation

1.  **Cloner le dépôt** (si applicable) ou naviguer dans le dossier du projet.

2.  **Créer un environnement virtuel** :
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Sur Linux/Mac
    # ou
    venv\Scripts\activate     # Sur Windows
    ```

3.  **Installer les dépendances** :
    ```bash
    pip install django djangorestframework requests tqdm
    ```

## Initialisation

1.  **Appliquer les migrations de base de données** :
    ```bash
    python manage.py migrate
    ```

2.  **Initialiser la structure de l'hôpital** (Pôles, Services, Lits) :
    ```bash
    python manage.py init_hospital
    ```

3.  **Créer un super-utilisateur** pour accéder à l'interface d'administration :
    ```bash
    python manage.py createsuperuser
    ```

## Utilisation

### 1. Lancer le Serveur Web

Le serveur web permet d'accéder à l'interface d'administration et à la page d'information de connexion.

```bash
python manage.py runserver
```

- **Dashboard Admin** : [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Info Connexion** : [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 2. Configurer un Client

Pour recevoir les données simulées :

1.  Allez dans le Dashboard Admin.
2.  Ajoutez un nouveau **Client**.
3.  Renseignez le **Nom** et la **Base URL** de votre application (ex: `http://localhost:3000`).
4.  Notez le **Client ID** et le **Client Secret** générés automatiquement.

Le simulateur enverra les requêtes POST à : `{Base URL}/api/webhook/fhir`

### 3. Lancer la Simulation

Dans un terminal séparé (avec l'environnement virtuel activé), lancez la boucle de simulation :

```bash
python manage.py run_simulation --interval 10
```

- `--interval` : Temps en secondes entre chaque événement (défaut : 10s).

Le script affichera les actions effectuées (Admission, Sortie, Observation) et le statut de l'envoi aux clients.

## Sécurité

Chaque requête envoyée par le simulateur contient les en-têtes suivants pour vérifier l'authenticité :

- `X-Client-ID`
- `X-Client-Secret`
