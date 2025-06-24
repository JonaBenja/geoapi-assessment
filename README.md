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
Deze lijst bevat  ook alleen maar locaties die de user zelf heeft aangemaakt.
De logica van de filter staat in het `filters.py` bestand. Ook heb ik testjes toegevoegd voor de werking van alle endpoints in `tests.py`.

Note: 
In de tests heb ik gebruik gemaakt van de modeule `factory_boy` omdat dit een hele fijne manier is om snel test instances aan te maken. Gaandeweg kwam ik erachter dat dat misschien voor deze assessment toch niet nodig bleek om deze module te gebruiken, maar ik heb het maar laten staan.

- Dynamische views/modellen
Voor deze feature heb ik een aparte branch gebruikt, `dynamic_models`, zodat ik een werkende `main` branch had voor de andere elementen. Je kunt op deze branch zien wat mijn aanpak was en hoe ver ik ben gekomen.

Mijn idee voor de feature was om het met het endpoint http://localhost:8000/locations/add_config/ via een POST request een JSON config file aan te leveren, waarna er dynamisch een nieuw model (een subclass van een nieuw model GeoLocationBase) zou worden gemaakt. Ook zou er dynamisch een serializer en een DRF ViewSet worden gemaakt en zou de endpoints geregistreerd moeten worden in de router.

Voorbeeld van een JSON config:

```
{
  "name": "Tree",
  "fields": {
    "species": "CharField",
    "planted_at": "DateTimeField"
  }
}
```

Het leek me leuk om bijvoorbeeld modellen te maken voor bomen, afvalbakken en bankjes in de stad.

Dit model zou dan op het endpoint http://localhost:8000/trees/ moeten verschijnen.

Ik liep vast bij het registreren van de views in de router: http://localhost:8000/trees/ bleek niet te bestaan.

Als ik meer tijd zou hebben gehad, zou ik:

- Een logger toevoegen zodat ik kan zien wat er gebeurt bij het aanmaken van het model (voornamelijk in `geoapi/utils/dynamic_models.py`)
- Een third party plug in gebruiken om te zien welke urls er toevoegd zijn in de router
- Eventueel apart base model maken (dus geen GeoLocationBase), maar de dynamische modellen toevoegen aan GeoLocation. GeoLocation nu laat alleen maar punten zien, en dat geeft niet zoveel informatie.
