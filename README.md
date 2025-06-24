# GeoLocation API assessment


## Installatie
- Maak een .env file aan op basis van de .env.example file.
- Run `docker compose build`
- Run `docker compose up`
- Run `docker compose exec web python manage.py migrate`
- Run `docker compose restart`

De applicatie moet nu beschikbaar zijn op de volgende url:
[http://localhost:8000/status](http://localhost:8000/status)

## Beschrijving project

### API endpoints
- http://localhost:8000/locations/
- http://localhost:8000/locations/add
- http://localhost:8000/locations/
- http://localhost:8000/locations/?reference_id=17&radius=1000

In progress (op branch `dynamic_models`):
- http://localhost:8000/locations/add_config/

### Aanpak en ontwerpkeuzes

- GET & POST endpoints
Voor de POST en GET endpoints heb ik een overzichtelijk `GeoLocation` model gemaakt.
Voor de views begon ik met een standaard APIListCreateView van DRF, om zoveel mogelijk gebruik te maken van de out-of-the-box functionaliteit.
Ik heb user authentication toegevoegd zodat alleen ingelogde users de GeoLocations konden bekijken en aanmaken, en de GeoLocations worden bij het aanmaken gekoppeld aan de ingelogde user. De user kan ook alleen de locaties bekijken die die zelf heeft aangemaakt.
Dit werkte in eerste instantie goed voor beide endpoints, maar toen ik de filtering feature wilde toevoegen moest ik dit aanpassen. 

- Afstandsfilter
Voor een mooie werkende afstandsfilder heb ik de APIListCreateViews gesplitst naar een aparte APIListView voor het bekijken van de locaties, en een APICreateView voor het aanmaken van een locatie.
De reden hiervoor was dat ik, naast het meegeven van query parameters in de url (http://localhost:8000/locations/?reference_id=17&radius=1000), het ook mogelijk wilde maken om met de `Filters` button in de DRF view de locatielijst te filteren.
Als je hierop klikt, kun je met een HTML form een referentiepunt en een straal invoeren, op 'Filter' klikken en dan verschijnt de gefilterde lijst.
Deze lijst bevat  ...
